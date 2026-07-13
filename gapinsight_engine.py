"""
=============================================================================
  GapInsight – Research Gap Detection & Recommendation System
  FILE 3: Python Bridge — Oracle + MongoDB + Gap Detection Engine
  Student: Kashaf Fayyaz | FA24-BAI-028
=============================================================================
  INSTALL:
    pip install pymongo oracledb scikit-learn nltk numpy

  NLTK data (first run only):
    import nltk
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

  RUN:
    python gapinsight_engine.py
=============================================================================
"""

import os
import re
import math
from datetime import datetime
from collections import Counter
from typing import List, Dict, Tuple

import numpy as np
from pymongo import MongoClient, DESCENDING

# Oracle — use oracledb (modern, no Instant Client needed for thin mode)
import oracledb

# NLP
import nltk
from nltk.corpus   import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem     import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise        import cosine_similarity

# ─── Download NLTK data (safe to call repeatedly) ─────────────────────────────
for pkg in ["stopwords", "punkt", "wordnet", "punkt_tab"]:
    try:
        nltk.download(pkg, quiet=True)
    except Exception:
        pass


# =============================================================================
#  CONFIGURATION  — change these to match your setup
# =============================================================================
ORACLE_USER     = "SYS"
ORACLE_PASSWORD = "12345"
ORACLE_DSN      = "localhost:1521/orclpdb"

MONGO_URI       = "mongodb://localhost:27017/"
MONGO_DB        = "gapinsight_db"


# =============================================================================
#  DATABASE CONNECTORS
# =============================================================================

class OracleDB:
    """Thin wrapper around oracledb for GapInsight queries."""

    def __init__(self):
        self.conn   = None
        self.cursor = None

    def connect(self):
        self.conn   = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN, mode=oracledb.AUTH_MODE_SYSDBA)
        self.cursor = self.conn.cursor()
        print("  ✓ Connected to Oracle")
        return self

    def disconnect(self):
        if self.cursor: self.cursor.close()
        if self.conn:   self.conn.close()

    # ── User operations ───────────────────────────────────────────────────────
    def get_user(self, user_id: int) -> Dict:
        self.cursor.execute(
            "SELECT user_id, name, email, role, created_at FROM Users WHERE user_id = :1",
            [user_id]
        )
        row = self.cursor.fetchone()
        if not row:
            return {}
        cols = [d[0].lower() for d in self.cursor.description]
        return dict(zip(cols, row))

    def get_user_profile(self, user_id: int) -> Dict:
        self.cursor.execute(
            """SELECT u.name, u.email, u.role,
                      p.university, p.department, p.research_interest
               FROM Users u
               LEFT JOIN User_Profile p ON u.user_id = p.user_id
               WHERE u.user_id = :1""",
            [user_id]
        )
        row = self.cursor.fetchone()
        if not row:
            return {}
        cols = [d[0].lower() for d in self.cursor.description]
        return dict(zip(cols, row))

    def get_all_users(self) -> List[Dict]:
        self.cursor.execute("SELECT user_id, name, email, role FROM Users ORDER BY user_id")
        cols = [d[0].lower() for d in self.cursor.description]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]

    def email_exists(self, email: str) -> bool:
        """Check if email already exists in database"""
        self.cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE email = :1", [email]
        )
        count = self.cursor.fetchone()[0]
        return count > 0

    # ── Bookmark operations ───────────────────────────────────────────────────
    def add_bookmark(self, user_id: int, paper_id: str, notes: str = "") -> bool:
        try:
            self.cursor.execute(
                "INSERT INTO Bookmarks (bookmark_id, user_id, paper_id, notes) VALUES (SEQ_BOOKMARK.NEXTVAL, :1, :2, :3)",
                [user_id, paper_id, notes]
            )
            self.conn.commit()
            self._log_action(user_id, "BOOKMARK", f"Bookmarked paper: {paper_id}")
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"  ✗ Bookmark error: {e}")
            return False

    def get_bookmarks(self, user_id: int) -> List[Dict]:
        self.cursor.execute(
            """SELECT bookmark_id, paper_id, notes, saved_at
               FROM Bookmarks WHERE user_id = :1
               ORDER BY saved_at DESC""",
            [user_id]
        )
        cols = [d[0].lower() for d in self.cursor.description]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]

    # ── Recommendation operations ─────────────────────────────────────────────
    def save_recommendation(self, user_id: int, topic: str,
                             score: float, category_id: int, reason: str) -> bool:
        try:
            self.cursor.execute(
                """INSERT INTO Recommendations (recommendation_id, user_id, topic, score, category_id, reason)
                   VALUES (SEQ_RECOMMENDATION.NEXTVAL, :1, :2, :3, :4, :5)""",
                [user_id, topic, round(score, 4), category_id, reason]
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"  ✗ Recommendation save error: {e}")
            return False

    def get_recommendations(self, user_id: int, limit: int = 5) -> List[Dict]:
        self.cursor.execute(
            """SELECT r.topic, r.score, r.reason, c.name AS category, r.generated_at
               FROM Recommendations r
               LEFT JOIN Categories c ON r.category_id = c.category_id
               WHERE r.user_id = :1
               ORDER BY r.score DESC
               FETCH FIRST :2 ROWS ONLY""",
            [user_id, limit]
        )
        cols = [d[0].lower() for d in self.cursor.description]
        return [dict(zip(cols, row)) for row in self.cursor.fetchall()]

    def save_gap(self, category_id: int, keyword: str,
                 paper_count: int, gap_score: float, description: str) -> bool:
        try:
            self.cursor.execute(
                """INSERT INTO Research_Gaps (gap_id, category_id, keyword, paper_count, gap_score, description)
                   VALUES (SEQ_GAP.NEXTVAL, :1, :2, :3, :4, :5)""",
                [category_id, keyword, paper_count, round(gap_score, 4), description]
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False

    def get_category_id(self, category_name: str) -> int:
        self.cursor.execute(
            "SELECT category_id FROM Categories WHERE name = :1", [category_name]
        )
        row = self.cursor.fetchone()
        return row[0] if row else 1     # default to category 1

    # ── Activity logging ──────────────────────────────────────────────────────
    def _log_action(self, user_id: int, action: str, detail: str = ""):
        try:
            self.cursor.execute(
                "INSERT INTO Activity_Log (log_id, user_id, action, detail) VALUES (SEQ_LOG.NEXTVAL, :1, :2, :3)",
                [user_id, action, detail[:500]]
            )
            self.conn.commit()
        except Exception:
            pass    # logging failure should never crash the app


class MongoDB:
    """Wrapper around pymongo for GapInsight collections."""

    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db     = self.client[MONGO_DB]
        print("  ✓ Connected to MongoDB")

    def disconnect(self):
        self.client.close()

    # ── Paper operations ──────────────────────────────────────────────────────
    def insert_paper(self, paper: Dict) -> str:
        """Insert a paper document, return the new ObjectId as string."""
        paper.setdefault("uploaded_at", datetime.utcnow())
        paper.setdefault("status",      "pending")
        result = self.db.papers.insert_one(paper)
        return str(result.inserted_id)

    def search_papers(self, query: str, category: str = None,
                      year_from: int = None, limit: int = 10) -> List[Dict]:
        """Full-text search with optional filters."""
        filt: Dict = {"$text": {"$search": query}}
        if category:  filt["category"] = category
        if year_from: filt["year"]     = {"$gte": year_from}

        projection = {"title": 1, "abstract": 1, "keywords": 1,
                      "category": 1, "year": 1, "citation_count": 1,
                      "score": {"$meta": "textScore"}}
        results = (
            self.db.papers
            .find(filt, projection)
            .sort([("score", {"$meta": "textScore"})])
            .limit(limit)
        )
        return [dict(r) for r in results]

    def get_paper(self, paper_id_str: str) -> Dict:
        from bson import ObjectId
        doc = self.db.papers.find_one({"_id": ObjectId(paper_id_str)})
        return dict(doc) if doc else {}

    def get_all_papers(self) -> List[Dict]:
        return list(self.db.papers.find({}, {"title": 1, "abstract": 1,
                                              "keywords": 1, "category": 1, "year": 1}))

    # ── Keyword operations ────────────────────────────────────────────────────
    def upsert_keyword(self, term: str, category: str,
                       frequency: int, gap_score: float):
        self.db.keywords.update_one(
            {"term": term, "category": category},
            {"$set": {"frequency": frequency, "gap_score": round(gap_score, 4),
                      "last_updated": datetime.utcnow()}},
            upsert=True
        )

    def get_top_gaps(self, limit: int = 10, category: str = None) -> List[Dict]:
        filt = {"category": category} if category else {}
        return list(
            self.db.keywords
            .find(filt, {"term": 1, "category": 1, "gap_score": 1, "frequency": 1, "trend": 1})
            .sort("gap_score", DESCENDING)
            .limit(limit)
        )

    # ── Cluster operations ────────────────────────────────────────────────────
    def save_cluster(self, cluster: Dict) -> str:
        cluster.setdefault("created_at", datetime.utcnow())
        cluster.setdefault("updated_at", datetime.utcnow())
        result = self.db.research_clusters.insert_one(cluster)
        return str(result.inserted_id)

    # ── Search history ────────────────────────────────────────────────────────
    def log_search(self, user_id: int, query: str, results_count: int):
        self.db.search_history.insert_one({
            "user_id":       user_id,
            "query":         query,
            "results_count": results_count,
            "filters":       {},
            "searched_at":   datetime.utcnow()
        })

    # ── Notes ─────────────────────────────────────────────────────────────────
    def add_note(self, user_id: int, paper_id_str: str, content: str,
                 tags: List[str] = None, is_private: bool = True) -> str:
        from bson import ObjectId
        result = self.db.notes.insert_one({
            "user_id":    user_id,
            "paper_id":   ObjectId(paper_id_str),
            "content":    content,
            "tags":       tags or [],
            "is_private": is_private,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        return str(result.inserted_id)


# =============================================================================
#  KEYWORD EXTRACTION ENGINE
# =============================================================================

class KeywordExtractor:
    """
    Extracts keywords from text using TF-IDF.
    No external NLP APIs needed — pure sklearn + NLTK.
    """

    def __init__(self):
        self.stop_words  = set(stopwords.words("english"))
        self.lemmatizer  = WordNetLemmatizer()
        self.vectorizer  = TfidfVectorizer(
            max_features=50,
            ngram_range=(1, 2),     # single words AND bigrams (e.g. "neural network")
            stop_words="english",
            min_df=1,
        )

    def clean_text(self, text: str) -> str:
        text   = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())
        tokens = word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens
                  if t not in self.stop_words and len(t) > 2]
        return " ".join(tokens)

    def extract_from_text(self, text: str, top_n: int = 15) -> List[Tuple[str, float]]:
        """Return [(keyword, tfidf_score)] for a single document."""
        cleaned = self.clean_text(text)
        if not cleaned.strip():
            return []
        matrix   = self.vectorizer.fit_transform([cleaned])
        feature  = self.vectorizer.get_feature_names_out()
        scores   = matrix.toarray()[0]
        pairs    = sorted(zip(feature, scores), key=lambda x: x[1], reverse=True)
        return [(kw, round(score, 4)) for kw, score in pairs[:top_n] if score > 0]

    def extract_from_papers(self, papers: List[Dict], top_n: int = 20) -> Dict[str, float]:
        """
        Run TF-IDF across multiple papers — finds terms important
        to the corpus but rare enough to signal a gap.
        Returns {keyword: gap_score}
        """
        if not papers:
            return {}
        corpus = [
            self.clean_text(f"{p.get('title','')} {p.get('abstract','')} "
                            f"{' '.join(p.get('keywords', []))}")
            for p in papers
        ]
        corpus = [c for c in corpus if c.strip()]
        if len(corpus) < 2:
            return self.extract_from_corpus_single(corpus[0] if corpus else "", top_n)

        vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2),
                                     stop_words="english")
        matrix  = vectorizer.fit_transform(corpus)
        feature = vectorizer.get_feature_names_out()

        # Average TF-IDF score across all documents
        avg_scores = np.asarray(matrix.mean(axis=0)).flatten()
        pairs      = sorted(zip(feature, avg_scores), key=lambda x: x[1], reverse=True)
        return {kw: round(float(s), 4) for kw, s in pairs[:top_n] if s > 0}

    def extract_from_corpus_single(self, text: str, top_n: int) -> Dict[str, float]:
        pairs = self.extract_from_text(text, top_n)
        return {kw: score for kw, score in pairs}


# =============================================================================
#  GAP DETECTION ENGINE  (Enhanced Multi-Factor Scoring)
# =============================================================================

class GapDetector:
    """
    Improved gap detection using 4 factors:
      1. Keyword frequency     — fewer papers = bigger gap
      2. Citation weight       — high-cited topic with few papers = real gap
      3. Recency bias          — old papers on a topic suggest stale coverage
      4. Category distribution — topic covered in only 1 category = narrow gap

    Gap score range: 0.0 (fully researched) → 1.0 (completely unexplored)
    """

    # Known high-impact topics that SHOULD have many papers — penalise if few
    HIGH_DEMAND_TOPICS = {
        "urdu nlp", "pashto nlp", "sindhi nlp", "arabic nlp",
        "low-resource nlp", "low resource nlp", "under-resourced",
        "tinyml", "edge ai", "on-device ml",
        "dental ai", "telemedicine ai", "mental health nlp",
        "underwater robot", "agricultural robot",
        "quantum ml", "spiking neural network",
        "continual learning", "catastrophic forgetting",
        "federated learning security", "iot security",
        "deepfake detection", "social engineering",
    }

    def __init__(self, oracle: OracleDB, mongo: MongoDB):
        self.oracle    = oracle
        self.mongo     = mongo
        self.extractor = KeywordExtractor()

    # ── Core scoring ──────────────────────────────────────────────────────────
    def _frequency_score(self, freq: int, max_freq: int) -> float:
        """Low frequency → high score. Log-scaled."""
        if max_freq == 0:
            return 1.0
        return 1.0 - (math.log1p(freq) / math.log1p(max_freq))

    def _citation_gap_score(self, keyword: str, papers: List[Dict]) -> float:
        """
        If papers covering this keyword have HIGH citations but there are FEW of them,
        that is a strong gap signal — the topic is important but under-studied.
        Returns 0.0–1.0.
        """
        matching = [p for p in papers
                    if keyword in " ".join(p.get("keywords", [])).lower()]
        if not matching:
            return 0.5   # neutral — no data
        avg_citations = sum(p.get("citation_count", 0) for p in matching) / len(matching)
        # Normalise: papers with >5000 avg citations get full score
        citation_score = min(avg_citations / 5000.0, 1.0)
        # Combine: few papers + high citations = high gap
        count_penalty  = 1.0 - min(len(matching) / 10.0, 1.0)   # 10+ papers = no penalty
        return round((citation_score * 0.6 + count_penalty * 0.4), 4)

    def _recency_score(self, keyword: str, papers: List[Dict]) -> float:
        """
        If the newest paper on this topic is old, it is under-researched recently.
        Recent papers (2022+) reduce the gap score.
        """
        current_year = datetime.utcnow().year
        matching_years = [p.get("year", 2000) for p in papers
                          if keyword in " ".join(p.get("keywords", [])).lower()]
        if not matching_years:
            return 0.6   # no papers = some gap
        newest = max(matching_years)
        age    = current_year - newest          # 0 = this year, 5 = 5 years old
        return round(min(age / 8.0, 1.0), 4)   # 8+ year old = max score

    def _demand_bonus(self, keyword: str) -> float:
        """Known under-researched topics get a bonus to surface them."""
        kw_lower = keyword.lower()
        for topic in self.HIGH_DEMAND_TOPICS:
            if topic in kw_lower or kw_lower in topic:
                return 0.15
        return 0.0

    def compute_gap_score(self, keyword: str, freq: int,
                          max_freq: int, papers: List[Dict]) -> float:
        """
        Weighted combination of all four factors:
          40% frequency score   — core signal
          25% citation gap      — importance vs coverage
          20% recency score     — how recent is the coverage
          15% demand bonus      — known important under-studied areas
        """
        f_score   = self._frequency_score(freq, max_freq)
        c_score   = self._citation_gap_score(keyword, papers)
        r_score   = self._recency_score(keyword, papers)
        d_bonus   = self._demand_bonus(keyword)

        raw = (f_score * 0.40) + (c_score * 0.25) + (r_score * 0.20) + d_bonus
        return round(min(raw, 1.0), 4)

    # ── Main pipeline ─────────────────────────────────────────────────────────
    def analyze_and_detect(self, category_filter: str = None) -> List[Dict]:
        """
        Full pipeline:
        1. Load papers from MongoDB
        2. Build keyword frequency table from paper metadata
        3. Compute multi-factor gap scores
        4. Filter noise (min 2-char keywords, skip stopwords)
        5. Save to MongoDB keywords + Oracle Research_Gaps
        Returns top gaps sorted by gap_score descending.
        """
        print("\n  [Gap Detection] Starting analysis…")

        # 1. Load papers
        papers = self.mongo.get_all_papers()
        if category_filter:
            papers = [p for p in papers if p.get("category") == category_filter]
        print(f"  [Gap Detection] Loaded {len(papers)} papers")

        if not papers:
            print("  [Gap Detection] No papers found.")
            return []

        # 2. Count keyword frequency from paper metadata keywords
        all_keywords: List[str] = []
        for p in papers:
            all_keywords.extend([kw.lower().strip()
                                  for kw in p.get("keywords", [])
                                  if len(kw.strip()) > 3])  # skip very short terms
        keyword_freq = Counter(all_keywords)

        # Remove extremely rare single-occurrence generic terms
        # Only keep: (a) appears 2+ times, OR (b) is a known high-demand topic
        filtered_freq = {}
        for kw, freq in keyword_freq.items():
            is_high_demand = any(t in kw for t in self.HIGH_DEMAND_TOPICS)
            if freq >= 2 or is_high_demand:
                filtered_freq[kw] = freq
            elif freq == 1 and len(kw.split()) >= 2:
                # Keep multi-word phrases even if appearing once
                filtered_freq[kw] = freq

        if not filtered_freq:
            filtered_freq = keyword_freq   # fallback

        max_freq = max(filtered_freq.values()) if filtered_freq else 1
        print(f"  [Gap Detection] Analysing {len(filtered_freq)} meaningful keywords…")

        # 3. Compute multi-factor gap scores
        results = []
        for kw, freq in filtered_freq.items():
            gap_score = self.compute_gap_score(kw, freq, max_freq, papers)
            category  = self._infer_category(kw, papers)
            results.append({
                "keyword":     kw,
                "frequency":   freq,
                "gap_score":   gap_score,
                "category":    category,
                "description": self._build_description(kw, freq, gap_score, papers),
            })

        results.sort(key=lambda x: x["gap_score"], reverse=True)

        # 4. Persist to MongoDB
        for r in results:
            self.mongo.upsert_keyword(r["keyword"], r["category"],
                                      r["frequency"], r["gap_score"])

        # 5. Persist top 30 to Oracle
        for r in results[:30]:
            cat_id = self.oracle.get_category_id(r["category"])
            self.oracle.save_gap(cat_id, r["keyword"], r["frequency"],
                                 r["gap_score"], r["description"])

        print(f"  [Gap Detection] Done. {len(results)} keywords scored.")
        print(f"  Top gap: '{results[0]['keyword']}'  "
              f"(score={results[0]['gap_score']:.4f}, "
              f"papers={results[0]['frequency']})")
        return results

    def _build_description(self, keyword: str, freq: int,
                            gap_score: float, papers: List[Dict]) -> str:
        """Human-readable explanation of why this is a gap."""
        matching = [p for p in papers
                    if keyword in " ".join(p.get("keywords", [])).lower()]
        newest   = max((p.get("year", 0) for p in matching), default=0)
        avg_cit  = int(sum(p.get("citation_count", 0) for p in matching)
                       / max(len(matching), 1))

        parts = [f"Only {freq} paper(s) cover '{keyword}'."]
        if newest and newest < 2020:
            parts.append(f"Last covered in {newest} — potentially outdated.")
        if avg_cit > 1000:
            parts.append(f"High avg citations ({avg_cit}) suggest demand exceeds supply.")
        if gap_score > 0.7:
            parts.append("Strong research gap — excellent dissertation/thesis opportunity.")
        elif gap_score > 0.5:
            parts.append("Moderate gap — room for novel contribution.")
        return " ".join(parts)

    def _infer_category(self, keyword: str, papers: List[Dict]) -> str:
        """Return the most common category among papers containing this keyword."""
        cats = [p.get("category", "General")
                for p in papers
                if keyword in " ".join(p.get("keywords", [])).lower()]
        if not cats:
            return "General"
        return Counter(cats).most_common(1)[0][0]


class Recommender:
    """
    Generates personalized research topic recommendations per user
    based on their search history, bookmarks, and current research gaps.
    """

    def __init__(self, oracle: OracleDB, mongo: MongoDB):
        self.oracle = oracle
        self.mongo  = mongo

    def generate_for_user(self, user_id: int, top_n: int = 5) -> List[Dict]:
        """
        Strategy:
        1. Get user's research interest from Oracle profile
        2. Get user's search history from MongoDB
        3. Find top gaps that match their interests
        4. Score and rank recommendations
        5. Save to Oracle Recommendations table
        """
        # 1. User profile
        profile = self.oracle.get_user_profile(user_id)
        interest = (profile.get("research_interest") or "").lower()

        # 2. Search history keywords
        history = list(
            self.mongo.db.search_history
            .find({"user_id": user_id}, {"query": 1})
            .sort("searched_at", DESCENDING)
            .limit(20)
        )
        history_text = " ".join([h.get("query", "") for h in history]).lower()

        # 3. Top gaps from MongoDB
        all_gaps = self.mongo.get_top_gaps(limit=50)

        # 4. Score each gap against user context
        recommendations = []
        for gap in all_gaps:
            term    = gap.get("term", "")
            cat     = gap.get("category", "")
            gscore  = gap.get("gap_score", 0)

            # Relevance: does term appear in user's interests or history?
            interest_match = 1.0 if term.lower() in interest    else 0.0
            history_match  = 1.0 if term.lower() in history_text else 0.0

            # Final score: gap quality (70%) + relevance (30%)
            final_score = (gscore * 0.7) + ((interest_match + history_match * 0.5) * 0.3)
            final_score = round(min(final_score, 1.0), 4)

            reason = (
                f"High research gap score ({gscore:.2f}) in {cat}."
                + (" Matches your research interest." if interest_match else "")
                + (" Relates to your recent searches." if history_match else "")
            )

            recommendations.append({
                "topic":       term,
                "score":       final_score,
                "gap_score":   gscore,
                "category":    cat,
                "reason":      reason,
            })

        recommendations.sort(key=lambda x: x["score"], reverse=True)
        top_recs = recommendations[:top_n]

        # 5. Save to Oracle
        for rec in top_recs:
            cat_id = self.oracle.get_category_id(rec["category"])
            self.oracle.save_recommendation(
                user_id, rec["topic"], rec["score"], cat_id, rec["reason"]
            )

        return top_recs


# =============================================================================
#  MAIN DEMO  — runs the full pipeline
# =============================================================================
def main():
    print("\n" + "=" * 65)
    print("  GapInsight — Full Pipeline Demo")
    print("=" * 65)

    # ── Connect ───────────────────────────────────────────────────────────────
    mongo = MongoDB()

    # Oracle connection (comment out if Oracle not set up yet)
    try:
        oracle = OracleDB().connect()
        oracle_ready = True
    except Exception as e:
        print(f"  ⚠ Oracle not connected ({e}) — running MongoDB-only mode")
        oracle_ready = False
        oracle       = None

    # ── Full-text paper search ─────────────────────────────────────────────────
    print("\n[1] Searching papers: 'transformer attention'")
    results = mongo.search_papers("transformer attention", limit=3)
    for r in results:
        print(f"    → {r.get('title','')} ({r.get('year','')})")

    # ── Gap detection ──────────────────────────────────────────────────────────
    print("\n[2] Running gap detection across all papers…")
    if oracle_ready:
        # Clear stale cached keywords so fresh scores are used
        mongo.db.keywords.drop()
        print("  ✓ Cleared stale keyword cache — fresh scores incoming")

        detector = GapDetector(oracle, mongo)
        gaps     = detector.analyze_and_detect()

        print(f"\n  Top 10 Research Gaps (fresh scores):")
        print(f"  {'Keyword':<38} {'Category':<28} {'Papers':>6}  {'Gap Score':>9}")
        print(f"  {'-'*38} {'-'*28} {'-'*6}  {'-'*9}")
        for g in gaps[:10]:
            print(f"  {g['keyword']:<38} {g['category']:<28} "
                  f"{g['frequency']:>6}  {g['gap_score']:>9.4f}")
    else:
        gaps = mongo.get_top_gaps(limit=5)
        print("  Top 5 Research Gaps (from MongoDB):")
        for g in gaps:
            print(f"    [{g['gap_score']:.4f}] {g['term']} — {g['frequency']} papers")

    # ── Recommendations — use freshly scored gaps ──────────────────────────────
    print("\n[3] Generating recommendations for user_id=1…")
    if oracle_ready:
        recommender = Recommender(oracle, mongo)
        recs        = recommender.generate_for_user(user_id=1, top_n=5)
        print("\n  Personalized Recommendations:")
        for i, r in enumerate(recs, 1):
            print(f"  #{i} [{r['score']:.4f}] {r['topic']}")
            print(f"       Gap score: {r['gap_score']:.4f} | {r['reason']}")
    else:
        recs = mongo.get_top_gaps(limit=5)
        print("  Top gap-based suggestions:")
        for r in recs:
            print(f"    → {r['term']} (gap={r['gap_score']:.4f})")

    # ── Add a new paper ────────────────────────────────────────────────────────
    print("\n[4] Uploading a new paper…")
    new_id = mongo.insert_paper({
        "title":               "Zero-Shot Learning for Low-Resource Languages",
        "abstract":            "This paper explores zero-shot cross-lingual transfer for languages with minimal training data, focusing on South Asian languages including Urdu and Sindhi.",
        "uploaded_by_user_id": 1,
        "keywords":            ["zero-shot learning", "low-resource NLP", "Urdu", "cross-lingual transfer", "Sindhi"],
        "category":            "Natural Language Processing",
        "year":                2024,
        "citation_count":      0,
        "language":            "English",
        "status":              "pending"
    })
    print(f"  ✓ Inserted paper with _id: {new_id}")

    # ── Log activity ───────────────────────────────────────────────────────────
    if oracle_ready:
        oracle._log_action(1, "UPLOAD", "Uploaded: zero_shot_low_resource.pdf")

    # ── Search history ─────────────────────────────────────────────────────────
    mongo.log_search(1, "zero-shot low-resource NLP", results_count=1)

    # ── Bookmarks ──────────────────────────────────────────────────────────────
    if oracle_ready:
        oracle.add_bookmark(1, new_id, "Very relevant to my GapInsight project!")
        bms = oracle.get_bookmarks(1)
        print(f"\n[5] User 1 bookmarks: {len(bms)} total")

    # ── Disconnect ─────────────────────────────────────────────────────────────
    mongo.disconnect()
    if oracle_ready:
        oracle.disconnect()

    print("\n" + "=" * 65)
    print("  Pipeline complete!")
    print("=" * 65)


import hashlib

# =============================================================================
#  AUTH FUNCTIONS  (login / register)
# =============================================================================

def hash_password(password: str) -> str:
    """SHA-256 hash a password — never store plain text."""
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(oracle: OracleDB, email: str, password: str) -> dict:
    """
    Verify email + password against Oracle Users table.
    Returns user dict on success, empty dict on failure.
    """
    password_hash = hash_password(password)
    oracle.cursor.execute(
        """SELECT user_id, name, email, role
           FROM Users
           WHERE email      = :1
             AND password_hash = :2
             AND is_active   = 1""",
        [email, password_hash]
    )
    row = oracle.cursor.fetchone()
    if row:
        return {"user_id": row[0], "name": row[1],
                "email":   row[2], "role": row[3]}
    return {}


def register_user(oracle: OracleDB,
                  name: str, email: str, password: str,
                  role: str = "Student",
                  university: str = "",
                  research_interest: str = "",
                  student_reg: str = "") -> dict:
    """
    Register a new user — inserts into Users + User_Profile + subclass table.
    Returns the new user dict on success.
    Raises RuntimeError with clear message if email already exists.
    """
    # First check if email already exists
    if oracle.email_exists(email):
        raise RuntimeError(f"Email '{email}' is already registered. Please use a different email or login.")
    
    password_hash = hash_password(password)
    
    try:
        # Get next user_id manually
        oracle.cursor.execute("SELECT SEQ_USER.NEXTVAL FROM DUAL")
        new_id = oracle.cursor.fetchone()[0]
        
        # Insert into Users with explicit ID
        oracle.cursor.execute(
            """INSERT INTO Users (user_id, name, email, password_hash, role)
               VALUES (:1, :2, :3, :4, :5)""",
            [new_id, name, email, password_hash, role]
        )

        # Insert profile
        oracle.cursor.execute(
            """INSERT INTO User_Profile (profile_id, user_id, university, research_interest)
               VALUES (SEQ_PROFILE.NEXTVAL, :1, :2, :3)""",
            [new_id, university, research_interest]
        )

        # Insert subclass row based on role
        if role == "Student":
            reg = student_reg or f"REG-{new_id}"
            oracle.cursor.execute(
                "INSERT INTO Student (user_id, student_reg_no) VALUES (:1, :2)",
                [new_id, reg]
            )
        elif role == "Researcher":
            oracle.cursor.execute(
                "INSERT INTO Researcher (user_id, research_area) VALUES (:1, :2)",
                [new_id, research_interest or "General"]
            )
        elif role == "Admin":
            oracle.cursor.execute(
                "INSERT INTO Admin_User (user_id) VALUES (:1)", [new_id]
            )

        oracle.conn.commit()
        oracle._log_action(new_id, "REGISTER", f"New user registered: {email}")
        return {"user_id": new_id, "name": name, "email": email, "role": role}

    except Exception as e:
        oracle.conn.rollback()
        error_msg = str(e)
        if "unique constraint" in error_msg.lower() or "dup_val" in error_msg.upper():
            raise RuntimeError(f"Email '{email}' is already registered. Please use a different email or login.")
        else:
            raise RuntimeError(f"Registration failed: {error_msg}")


# =============================================================================
#  LOGIN TEST  — run standalone to test auth before UI
# =============================================================================

def test_login():
    print("\n" + "=" * 65)
    print("  GapInsight — User Auth Test")
    print("=" * 65)

    oracle = OracleDB().connect()

    # ── First: update existing user with a proper hashed password ────────────
    print("\n[SETUP] Setting hashed passwords for test users…")
    test_users = [
        ("kashaf@uni.edu",          "kashaf123"),
        ("shahid@uni.edu",          "shahid123"),
        ("sara@uni.edu",            "sara123"),
        ("admin@gapinsight.com",    "admin123"),
    ]
    for email, pwd in test_users:
        hashed = hash_password(pwd)
        oracle.cursor.execute(
            "UPDATE Users SET password_hash = :1 WHERE email = :2",
            [hashed, email]
        )
    oracle.conn.commit()
    print("  ✓ Passwords updated with SHA-256 hashes")

    # ── Test 1: Correct credentials ───────────────────────────────────────────
    print("\n[TEST 1] Login with CORRECT credentials")
    user = login_user(oracle, "kashaf@uni.edu", "kashaf123")
    if user:
        print(f"  ✓ Login SUCCESS")
        print(f"    user_id : {user['user_id']}")
        print(f"    name    : {user['name']}")
        print(f"    email   : {user['email']}")
        print(f"    role    : {user['role']}")
    else:
        print("  ✗ Login FAILED — check credentials")

    # ── Test 2: Wrong password ────────────────────────────────────────────────
    print("\n[TEST 2] Login with WRONG password")
    user2 = login_user(oracle, "kashaf@uni.edu", "wrongpassword")
    if not user2:
        print("  ✓ Correctly rejected wrong password")
    else:
        print("  ✗ Should have rejected wrong password!")

    # ── Test 3: Non-existent user ─────────────────────────────────────────────
    print("\n[TEST 3] Login with non-existent email")
    user3 = login_user(oracle, "nobody@test.com", "test123")
    if not user3:
        print("  ✓ Correctly rejected unknown email")
    else:
        print("  ✗ Should have rejected unknown user!")

    # ── Test 4: Register a brand new user ─────────────────────────────────────
    print("\n[TEST 4] Register a new user")
    try:
        new_user = register_user(
            oracle,
            name               = "Test Student",
            email              = "teststudent@uni.edu",
            password           = "testpass123",
            role               = "Student",
            university         = "FAST NUCES",
            research_interest  = "Computer Vision",
            student_reg        = "FA24-TEST-001"
        )
        print(f"  ✓ Registration SUCCESS")
        print(f"    user_id : {new_user['user_id']}")
        print(f"    name    : {new_user['name']}")
        print(f"    role    : {new_user['role']}")

        # Immediately login with new account
        login_check = login_user(oracle, "teststudent@uni.edu", "testpass123")
        if login_check:
            print(f"  ✓ New user can login immediately")
        else:
            print(f"  ✗ New user login failed")

    except RuntimeError as e:
        print(f"  ℹ  {e}")

    # ── Test 5: Duplicate registration (should show proper error) ─────────────
    print("\n[TEST 5] Try to register duplicate email")
    try:
        register_user(oracle, "Duplicate", "kashaf@uni.edu",
                      "anypassword", "Student")
        print("  ✗ Should have rejected duplicate email!")
    except RuntimeError as e:
        print(f"  ✓ Correctly rejected duplicate email: {e}")

    # ── Test 6: All users in system ───────────────────────────────────────────
    print("\n[TEST 6] All users currently in the system:")
    users = oracle.get_all_users()
    print(f"  {'ID':<5} {'Name':<25} {'Email':<35} {'Role'}")
    print(f"  {'-'*5} {'-'*25} {'-'*35} {'-'*12}")
    for u in users:
        print(f"  {u['user_id']:<5} {u['name']:<25} {u['email']:<35} {u['role']}")

    oracle.disconnect()
    print("\n" + "=" * 65)
    print("  Auth test complete! All functions working correctly.")
    print("  You are ready to build the UI.")
    print("=" * 65)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test_login":
        test_login()
    else:
        main()