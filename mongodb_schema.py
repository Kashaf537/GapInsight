"""
=============================================================================
  GapInsight – Research Gap Detection & Recommendation System
  FILE 2: MongoDB Schema, Validators & Sample Data  (CSC371 – Database Systems)
  Student: Kashaf Fayyaz | FA24-BAI-028
=============================================================================
  HOW TO RUN:
    1. Make sure MongoDB is running:  mongod  (or use MongoDB Atlas)
    2. Install driver:  pip install pymongo
    3. Run this file:   python mongodb_schema.py
=============================================================================
"""

from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from pymongo.errors import CollectionInvalid, DuplicateKeyError
from datetime import datetime
from bson import ObjectId
import json

# =============================================================================
#  CONNECTION
#  Change the URI to your MongoDB Atlas connection string if using cloud
# =============================================================================
MONGO_URI = "mongodb://localhost:27017/"   # local
# MONGO_URI = "mongodb+srv://<user>:<pass>@cluster.mongodb.net/"  # Atlas

client = MongoClient(MONGO_URI)
db     = client["gapinsight_db"]

print("=" * 65)
print("  GapInsight — MongoDB Schema Setup")
print("=" * 65)


# =============================================================================
#  HELPER: drop & recreate a collection cleanly
# =============================================================================
def reset_collection(name: str):
    if name in db.list_collection_names():
        db[name].drop()
        print(f"  ✓ Dropped existing collection: {name}")


# =============================================================================
#  1. PAPERS COLLECTION
#  Stores full research paper content + metadata
# =============================================================================
reset_collection("papers")

db.create_collection("papers", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["title", "abstract", "uploaded_by_user_id", "uploaded_at"],
        "properties": {
            "title": {
                "bsonType": "string",
                "description": "Paper title — required"
            },
            "abstract": {
                "bsonType": "string",
                "description": "Full abstract text — required"
            },
            "full_text": {
                "bsonType": "string",
                "description": "Entire paper body (optional — may be large)"
            },
            "uploaded_by_user_id": {
                "bsonType": "int",
                "description": "Oracle Users.user_id of the uploader"
            },
            "uploaded_at": {
                "bsonType": "date"
            },
            "keywords": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "Multi-valued attribute: list of extracted keywords"
            },
            "category": {
                "bsonType": "string",
                "description": "Research domain (matches Oracle Categories.name)"
            },
            "year": {
                "bsonType": "int",
                "minimum": 1900,
                "maximum": 2100
            },
            "doi": {
                "bsonType": "string",
                "description": "Digital Object Identifier"
            },
            "file_url": {
                "bsonType": "string",
                "description": "Path or URL to original PDF"
            },
            "citation_count": {
                "bsonType": "int",
                "minimum": 0
            },
            "language": {
                "bsonType": "string"
            },
            "status": {
                "bsonType": "string",
                "enum": ["pending", "indexed", "rejected"],
                "description": "Processing status"
            }
        }
    }
})
print("  ✓ Created collection: papers")

# Indexes on papers
papers = db["papers"]
papers.create_index([("title", TEXT), ("abstract", TEXT), ("keywords", TEXT)],
                    name="papers_text_search",
                    weights={"title": 10, "abstract": 5, "keywords": 3})
papers.create_index([("uploaded_by_user_id", ASCENDING)], name="papers_uploader")
papers.create_index([("category", ASCENDING)],             name="papers_category")
papers.create_index([("year", DESCENDING)],                name="papers_year")
papers.create_index([("doi", ASCENDING)], unique=True, sparse=True, name="papers_doi")
print("  ✓ Indexes created: papers")


# =============================================================================
#  2. KEYWORDS COLLECTION
#  Aggregated keyword frequency table — core of gap detection
# =============================================================================
reset_collection("keywords")

db.create_collection("keywords", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["term", "category", "frequency"],
        "properties": {
            "term": {
                "bsonType": "string",
                "description": "The keyword or phrase"
            },
            "category": {
                "bsonType": "string",
                "description": "Research domain this keyword belongs to"
            },
            "frequency": {
                "bsonType": "int",
                "minimum": 0,
                "description": "How many papers contain this keyword"
            },
            "gap_score": {
                "bsonType": "double",
                "minimum": 0.0,
                "maximum": 1.0,
                "description": "Computed gap score: 1.0 = complete gap, 0.0 = saturated"
            },
            "trend": {
                "bsonType": "string",
                "enum": ["rising", "stable", "declining"],
                "description": "Keyword trend direction"
            },
            "related_terms": {
                "bsonType": "array",
                "items": {"bsonType": "string"}
            },
            "last_updated": {
                "bsonType": "date"
            }
        }
    }
})
keywords = db["keywords"]
keywords.create_index([("term", ASCENDING), ("category", ASCENDING)],
                      unique=True, name="kw_term_category")
keywords.create_index([("gap_score", DESCENDING)],  name="kw_gap_score")
keywords.create_index([("frequency", ASCENDING)],   name="kw_frequency")
keywords.create_index([("term", TEXT)],              name="kw_text")
print("  ✓ Created collection: keywords")


# =============================================================================
#  3. RESEARCH_CLUSTERS COLLECTION
#  Groups of related papers sharing similar topics
# =============================================================================
reset_collection("research_clusters")

db.create_collection("research_clusters", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["cluster_name", "keywords", "paper_ids"],
        "properties": {
            "cluster_name": {"bsonType": "string"},
            "keywords": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "Dominant keywords defining the cluster"
            },
            "paper_ids": {
                "bsonType": "array",
                "items": {"bsonType": "objectId"},
                "description": "Papers belonging to this cluster"
            },
            "centroid_vector": {
                "bsonType": "array",
                "items": {"bsonType": "double"},
                "description": "TF-IDF centroid vector for this cluster"
            },
            "size": {
                "bsonType": "int",
                "minimum": 1
            },
            "gap_areas": {
                "bsonType": "array",
                "items": {"bsonType": "string"},
                "description": "Identified gaps within this cluster"
            },
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"}
        }
    }
})
clusters = db["research_clusters"]
clusters.create_index([("cluster_name", ASCENDING)], unique=True, name="cluster_name")
clusters.create_index([("keywords", ASCENDING)],               name="cluster_keywords")
print("  ✓ Created collection: research_clusters")


# =============================================================================
#  4. NOTES COLLECTION
#  User annotations on papers
# =============================================================================
reset_collection("notes")

db.create_collection("notes", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "paper_id", "content"],
        "properties": {
            "user_id":    {"bsonType": "int"},
            "paper_id":   {"bsonType": "objectId"},
            "content":    {"bsonType": "string"},
            "tags": {
                "bsonType": "array",
                "items": {"bsonType": "string"}
            },
            "is_private": {"bsonType": "bool"},
            "created_at": {"bsonType": "date"},
            "updated_at": {"bsonType": "date"}
        }
    }
})
notes = db["notes"]
notes.create_index([("user_id", ASCENDING), ("paper_id", ASCENDING)], name="notes_user_paper")
notes.create_index([("content", TEXT)], name="notes_text")
print("  ✓ Created collection: notes")


# =============================================================================
#  5. SEARCH_HISTORY COLLECTION
#  Every user query stored for personalization
# =============================================================================
reset_collection("search_history")

db.create_collection("search_history", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["user_id", "query", "searched_at"],
        "properties": {
            "user_id":       {"bsonType": "int"},
            "query":         {"bsonType": "string"},
            "results_count": {"bsonType": "int", "minimum": 0},
            "filters": {
                "bsonType": "object",
                "description": "Applied search filters as key-value pairs"
            },
            "clicked_paper_ids": {
                "bsonType": "array",
                "items": {"bsonType": "objectId"}
            },
            "searched_at":   {"bsonType": "date"}
        }
    }
})
search_history = db["search_history"]
search_history.create_index([("user_id", ASCENDING)],          name="sh_user")
search_history.create_index([("searched_at", DESCENDING)],     name="sh_date")
search_history.create_index([("query", TEXT)],                 name="sh_text")
# TTL index: auto-delete search history older than 90 days (90*24*3600 = 7776000 sec)
search_history.create_index([("searched_at", ASCENDING)],
                             expireAfterSeconds=7776000, name="sh_ttl")
print("  ✓ Created collection: search_history")


# =============================================================================
#  SAMPLE DATA
# =============================================================================
print("\n  Inserting sample data…")

# ── Papers ────────────────────────────────────────────────────────────────────
paper_docs = [
    {
        "title":              "Attention Is All You Need",
        "abstract":           "We propose the Transformer, a model architecture based solely on attention mechanisms. The Transformer outperforms all previously reported models on English-to-German and English-to-French translation tasks.",
        "full_text":          "1. Introduction The dominant sequence transduction models are based on complex recurrent or convolutional neural networks...",
        "uploaded_by_user_id": 1,
        "uploaded_at":        datetime(2017, 6, 12),
        "keywords":           ["transformer", "attention mechanism", "NLP", "neural network", "sequence modeling"],
        "category":           "Natural Language Processing",
        "year":               2017,
        "doi":                "10.48550/arXiv.1706.03762",
        "citation_count":     75000,
        "language":           "English",
        "status":             "indexed"
    },
    {
        "title":              "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding",
        "abstract":           "We introduce BERT, which stands for Bidirectional Encoder Representations from Transformers. BERT achieves state-of-the-art results on eleven NLP tasks.",
        "full_text":          "1. Introduction Language model pre-training has been shown to be effective for improving many natural language processing tasks...",
        "uploaded_by_user_id": 2,
        "uploaded_at":        datetime(2018, 10, 11),
        "keywords":           ["BERT", "pre-training", "transformers", "NLP", "language understanding", "fine-tuning"],
        "category":           "Natural Language Processing",
        "year":               2018,
        "doi":                "10.48550/arXiv.1810.04805",
        "citation_count":     50000,
        "language":           "English",
        "status":             "indexed"
    },
    {
        "title":              "Federated Learning: Strategies for Improving Communication Efficiency",
        "abstract":           "We present two practical methods (FedAvg and structured/sketched updates) for reducing the communication costs of federated learning.",
        "uploaded_by_user_id": 1,
        "uploaded_at":        datetime(2016, 10, 24),
        "keywords":           ["federated learning", "distributed ML", "communication efficiency", "privacy"],
        "category":           "Machine Learning",
        "year":               2016,
        "doi":                "10.48550/arXiv.1610.05492",
        "citation_count":     4200,
        "language":           "English",
        "status":             "indexed"
    },
    {
        "title":              "Research Gaps in Urdu Natural Language Processing: A Survey",
        "abstract":           "This survey identifies critical research gaps in Urdu NLP. Despite over 230 million speakers, Urdu remains severely under-resourced in NLP research.",
        "uploaded_by_user_id": 3,
        "uploaded_at":        datetime(2022, 3, 15),
        "keywords":           ["Urdu NLP", "low-resource NLP", "morphological analysis", "Urdu corpus", "sentiment analysis Urdu"],
        "category":           "Natural Language Processing",
        "year":               2022,
        "doi":                None,
        "citation_count":     45,
        "language":           "English",
        "status":             "indexed"
    },
    {
        "title":              "3D Medical Image Segmentation Using Deep Learning: Open Challenges",
        "abstract":           "We review deep learning methods for 3D medical image segmentation and identify key open research challenges including limited labeled data and real-time inference.",
        "uploaded_by_user_id": 2,
        "uploaded_at":        datetime(2021, 7, 8),
        "keywords":           ["3D segmentation", "medical imaging", "MRI", "deep learning", "U-Net"],
        "category":           "Computer Vision",
        "year":               2021,
        "doi":                "10.1016/j.media.2021.101934",
        "citation_count":     320,
        "language":           "English",
        "status":             "indexed"
    },
]

result     = papers.insert_many(paper_docs)
paper_ids  = result.inserted_ids
print(f"  ✓ Inserted {len(paper_ids)} papers")


# ── Keywords (aggregated frequency table) ────────────────────────────────────
keyword_docs = [
    {"term": "transformer",           "category": "Natural Language Processing", "frequency": 4200, "gap_score": 0.05, "trend": "rising",   "related_terms": ["attention mechanism", "BERT", "GPT"],             "last_updated": datetime.utcnow()},
    {"term": "Urdu NLP",              "category": "Natural Language Processing", "frequency": 12,   "gap_score": 0.91, "trend": "rising",   "related_terms": ["low-resource NLP", "Urdu corpus", "Urdu ASR"],     "last_updated": datetime.utcnow()},
    {"term": "federated learning",    "category": "Machine Learning",            "frequency": 340,  "gap_score": 0.55, "trend": "rising",   "related_terms": ["distributed ML", "privacy ML", "edge computing"],  "last_updated": datetime.utcnow()},
    {"term": "3D MRI segmentation",   "category": "Computer Vision",             "frequency": 28,   "gap_score": 0.78, "trend": "stable",   "related_terms": ["medical imaging", "U-Net 3D", "MRI analysis"],      "last_updated": datetime.utcnow()},
    {"term": "multimodal learning",   "category": "Machine Learning",            "frequency": 180,  "gap_score": 0.48, "trend": "rising",   "related_terms": ["vision-language", "CLIP", "image captioning"],      "last_updated": datetime.utcnow()},
    {"term": "explainable AI",        "category": "Machine Learning",            "frequency": 620,  "gap_score": 0.32, "trend": "rising",   "related_terms": ["XAI", "interpretability", "model explanation"],     "last_updated": datetime.utcnow()},
    {"term": "edge AI",               "category": "Machine Learning",            "frequency": 95,   "gap_score": 0.72, "trend": "rising",   "related_terms": ["TinyML", "model compression", "on-device AI"],      "last_updated": datetime.utcnow()},
    {"term": "code generation LLM",   "category": "Natural Language Processing", "frequency": 210,  "gap_score": 0.44, "trend": "rising",   "related_terms": ["Codex", "GitHub Copilot", "program synthesis"],    "last_updated": datetime.utcnow()},
]
keywords.insert_many(keyword_docs)
print(f"  ✓ Inserted {len(keyword_docs)} keywords")


# ── Research Clusters ─────────────────────────────────────────────────────────
cluster_docs = [
    {
        "cluster_name": "Transformer & Attention Models",
        "keywords":     ["transformer", "attention", "BERT", "GPT", "fine-tuning"],
        "paper_ids":    [paper_ids[0], paper_ids[1]],
        "size":         2,
        "gap_areas":    ["Urdu transformers", "low-resource transformer pre-training", "efficient attention for mobile"],
        "created_at":   datetime.utcnow(),
        "updated_at":   datetime.utcnow()
    },
    {
        "cluster_name": "Federated & Privacy-Preserving ML",
        "keywords":     ["federated learning", "differential privacy", "secure aggregation"],
        "paper_ids":    [paper_ids[2]],
        "size":         1,
        "gap_areas":    ["federated NLP for healthcare", "cross-silo federated vision models"],
        "created_at":   datetime.utcnow(),
        "updated_at":   datetime.utcnow()
    },
    {
        "cluster_name": "Medical Computer Vision",
        "keywords":     ["3D segmentation", "MRI", "CT scan", "U-Net"],
        "paper_ids":    [paper_ids[4]],
        "size":         1,
        "gap_areas":    ["real-time 3D MRI segmentation", "few-shot medical segmentation"],
        "created_at":   datetime.utcnow(),
        "updated_at":   datetime.utcnow()
    },
]
clusters.insert_many(cluster_docs)
print(f"  ✓ Inserted {len(cluster_docs)} research clusters")


# ── Notes ─────────────────────────────────────────────────────────────────────
note_docs = [
    {
        "user_id":    1,
        "paper_id":   paper_ids[0],
        "content":    "This paper introduces the Transformer. Key insight: replace RNNs with self-attention entirely. Very relevant to GapInsight keyword extraction.",
        "tags":       ["important", "architecture", "reference"],
        "is_private": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "user_id":    3,
        "paper_id":   paper_ids[3],
        "content":    "Urdu NLP is severely under-resourced. This could be a major research direction for our lab.",
        "tags":       ["gap", "Urdu", "priority"],
        "is_private": False,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
]
notes.insert_many(note_docs)
print(f"  ✓ Inserted {len(note_docs)} notes")


# ── Search History ────────────────────────────────────────────────────────────
search_docs = [
    {"user_id": 1, "query": "research gap detection NLP",        "results_count": 12, "filters": {"year_from": 2018}, "clicked_paper_ids": [paper_ids[1]], "searched_at": datetime.utcnow()},
    {"user_id": 1, "query": "transformer attention mechanism",   "results_count": 45, "filters": {},                  "clicked_paper_ids": [paper_ids[0]], "searched_at": datetime.utcnow()},
    {"user_id": 3, "query": "Urdu sentiment analysis",          "results_count": 3,  "filters": {"category": "NLP"}, "clicked_paper_ids": [paper_ids[3]], "searched_at": datetime.utcnow()},
    {"user_id": 2, "query": "federated learning privacy",       "results_count": 8,  "filters": {},                  "clicked_paper_ids": [paper_ids[2]], "searched_at": datetime.utcnow()},
]
search_history.insert_many(search_docs)
print(f"  ✓ Inserted {len(search_docs)} search history records")


# =============================================================================
#  USEFUL QUERIES  (run these to test your collections)
# =============================================================================
print("\n" + "=" * 65)
print("  VERIFICATION QUERIES")
print("=" * 65)

# 1. Full-text search for "transformer"
print("\n[1] Full-text search: 'transformer'")
results = papers.find({"$text": {"$search": "transformer"}},
                       {"title": 1, "score": {"$meta": "textScore"}}) \
                .sort([("score", {"$meta": "textScore"})]) \
                .limit(3)
for r in results:
    print(f"    → {r['title']}")

# 2. Top 5 research gaps (highest gap_score)
print("\n[2] Top 5 research gaps")
gaps = keywords.find({}, {"term": 1, "category": 1, "gap_score": 1, "frequency": 1}) \
               .sort("gap_score", DESCENDING).limit(5)
for g in gaps:
    print(f"    → [{g['gap_score']:.2f}] {g['term']} ({g['category']}) — {g['frequency']} papers")

# 3. Papers uploaded by user_id = 1
print("\n[3] Papers by user_id=1")
user_papers = papers.find({"uploaded_by_user_id": 1}, {"title": 1, "year": 1, "category": 1})
for p in user_papers:
    print(f"    → {p['title']} ({p['year']}) — {p['category']}")

# 4. Clusters with gap areas
print("\n[4] Research clusters & their gaps")
for c in clusters.find({}, {"cluster_name": 1, "gap_areas": 1, "size": 1}):
    print(f"    → {c['cluster_name']} ({c['size']} papers)")
    for g in c.get("gap_areas", []):
        print(f"       ◦ {g}")

# 5. Count by collection
print("\n[5] Collection counts")
for col_name in ["papers", "keywords", "research_clusters", "notes", "search_history"]:
    print(f"    {col_name:<22}: {db[col_name].estimated_document_count()} documents")

print("\n" + "=" * 65)
print("  MongoDB schema setup complete!")
print("  Database: gapinsight_db")
print("  Collections: papers, keywords, research_clusters, notes, search_history")
print("=" * 65)

client.close()