"""
=============================================================================
  GapInsight — Research Gap Detection System  (Professional Theme)
  Run: pip install flask flask-cors pymongo oracledb scikit-learn nltk numpy
       python app2.py
  Open: http://localhost:5000
=============================================================================
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime
import traceback, hashlib

try:
    from gapinsight_engine import (
        OracleDB, MongoDB, KeywordExtractor,
        GapDetector, Recommender, hash_password,
        login_user, register_user
    )
    ENGINE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import gapinsight_engine: {e}")
    ENGINE_AVAILABLE = False

app = Flask(__name__)
app.secret_key = "gapinsight_secret_key_2024"
CORS(app)

oracle = None
mongo  = None

def get_db_connections():
    global oracle, mongo
    if not ENGINE_AVAILABLE:
        return None, None
    try:
        if oracle is None:
            oracle = OracleDB().connect()
        if mongo is None:
            mongo = MongoDB()
        return oracle, mongo
    except Exception as e:
        print(f"DB connection error: {e}")
        return None, None

DEMO_PAPERS = [
    {"title": "Attention Is All You Need",                          "year": 2017, "category": "Natural Language Processing", "keywords": ["transformer","attention mechanism"], "citation_count": 75000,  "abstract": "We propose the Transformer, a model architecture based solely on attention mechanisms, dispensing with recurrence entirely."},
    {"title": "BERT: Pre-training of Deep Bidirectional Transformers","year": 2018,"category": "Natural Language Processing", "keywords": ["BERT","transformers","fine-tuning"], "citation_count": 50000,  "abstract": "We introduce BERT, which stands for Bidirectional Encoder Representations from Transformers."},
    {"title": "GPT-3: Language Models are Few-Shot Learners",        "year": 2020, "category": "Natural Language Processing", "keywords": ["GPT-3","language model","few-shot"],  "citation_count": 22000,  "abstract": "Scaling language models greatly improves task-agnostic few-shot performance."},
    {"title": "Federated Learning: Strategies for Communication",    "year": 2016, "category": "Machine Learning",            "keywords": ["federated learning","distributed ML"], "citation_count": 4200,   "abstract": "Two practical methods for reducing communication costs of federated learning."},
    {"title": "Research Gaps in Urdu Natural Language Processing",   "year": 2022, "category": "Natural Language Processing", "keywords": ["Urdu NLP","low-resource"],            "citation_count": 45,     "abstract": "Survey identifying critical research gaps in Urdu NLP despite its large speaker base."},
    {"title": "Deep Residual Learning for Image Recognition",        "year": 2016, "category": "Computer Vision",             "keywords": ["ResNet","residual learning","CNN"],   "citation_count": 120000, "abstract": "Residual learning framework to ease training of very deep neural networks."},
    {"title": "TinyML: Machine Learning on Embedded Systems",        "year": 2021, "category": "Machine Learning",            "keywords": ["TinyML","edge AI","quantization"],    "citation_count": 560,    "abstract": "Survey of TinyML methods and challenges for resource-constrained edge devices."},
    {"title": "AlphaFold: Protein Structure Prediction",            "year": 2021, "category": "Healthcare AI",               "keywords": ["AlphaFold","protein folding"],        "citation_count": 14000,  "abstract": "AlphaFold produces highly accurate protein structure predictions using deep learning."},
]

class TopicAnalyzer:
    def __init__(self, mongo_conn=None):
        self.mongo = mongo_conn

    def analyze_topic(self, topic, category=None):
        topic_lower = topic.lower().strip()
        if self.mongo is not None and ENGINE_AVAILABLE:
            try:
                all_papers     = self.mongo.get_all_papers()
                related_papers = [p for p in all_papers
                                  if topic_lower in p.get('title','').lower()
                                  or topic_lower in p.get('abstract','').lower()
                                  or any(topic_lower in kw.lower() for kw in p.get('keywords',[]))]
                paper_count    = len(related_papers)
                papers_data    = [{"title": p.get('title','Untitled'), "year": p.get('year','N/A'),
                                   "abstract": p.get('abstract','')[:300], "keywords": p.get('keywords',[]),
                                   "citation_count": p.get('citation_count',0),
                                   "category": p.get('category','Unknown'), "id": str(p.get('_id',''))}
                                  for p in related_papers[:10]]
                total = len(all_papers)
            except Exception as e:
                print(f"DB error: {e}"); return self._demo_analysis(topic)
        else:
            return self._demo_analysis(topic)

        if paper_count == 0:
            status,desc,color,gap_score = "Severely Under-Researched","No papers found. This represents a significant research opportunity.","critical",0.95
        elif paper_count <= 3:
            status,desc,color,gap_score = "Under-Researched",f"Only {paper_count} paper(s) found. This area warrants further investigation.","high",0.80
        elif paper_count <= 10:
            status,desc,color,gap_score = "Moderately Researched",f"{paper_count} papers found. Moderate research activity detected.","moderate",0.55
        elif paper_count <= 30:
            status,desc,color,gap_score = "Well Researched",f"{paper_count} papers found. This topic has reasonable coverage.","low",0.35
        else:
            status,desc,color,gap_score = "Saturated Topic",f"{paper_count} papers found. This topic is highly covered in the literature.","saturated",0.15

        return {"topic": topic, "paper_count": paper_count, "status_text": status,
                "status_desc": desc, "color": color, "gap_score": round(gap_score,4),
                "related_papers": papers_data, "total_papers_in_db": total}

    def _demo_analysis(self, topic):
        topic_lower = topic.lower()
        related     = [p for p in DEMO_PAPERS
                       if topic_lower in p['title'].lower()
                       or any(topic_lower in kw.lower() for kw in p['keywords'])]
        count = len(related)
        if count == 0:
            status,desc,color,gap_score = "Severely Under-Researched","No papers found. This represents a significant research opportunity.","critical",0.95
        elif count <= 3:
            status,desc,color,gap_score = "Under-Researched",f"Only {count} paper(s) found. This area warrants further investigation.","high",0.80
        elif count <= 10:
            status,desc,color,gap_score = "Moderately Researched",f"{count} papers found. Moderate research activity.","moderate",0.55
        else:
            status,desc,color,gap_score = "Saturated Topic",f"{count} papers found. Highly covered in literature.","saturated",0.15
        papers_data = [{"title":p["title"],"year":p["year"],"abstract":p["abstract"][:300],
                        "keywords":p["keywords"],"citation_count":p["citation_count"],
                        "category":p["category"],"id":f"demo_{p['title'][:12].replace(' ','_')}"}
                       for p in related]
        return {"topic":topic,"paper_count":count,"status_text":status,"status_desc":desc,
                "color":color,"gap_score":gap_score,"related_papers":papers_data,
                "total_papers_in_db":len(DEMO_PAPERS)}

# =============================================================================
#  LOGIN PAGE — PROFESSIONAL SLATE + GOLD THEME
# =============================================================================
LOGIN_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>GapInsight — Sign In</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0b0f1a;--s1:#111827;--s2:#1a2235;--s3:#0e1520;
  --bdr:#1e2d42;--bdr2:#2a3d58;
  --tx:#e8eef6;--mu:#6b80a0;--dim:#94a8c4;
  --gold:#c9a84c;--gold2:#e8c76a;--gold3:#a07830;
  --blue:#3b7dd8;--red:#e05555;--grn:#3aab6e;
  --ff:'IBM Plex Sans',sans-serif;--fm:'IBM Plex Mono',monospace;
  --r:8px;--rs:5px
}
body{background:var(--bg);color:var(--tx);font-family:var(--ff);min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;letter-spacing:.01em}
/* background pattern */
body::before{content:'';position:fixed;inset:0;background-image:radial-gradient(circle at 20% 20%,rgba(201,168,76,.06) 0%,transparent 50%),radial-gradient(circle at 80% 80%,rgba(59,125,216,.05) 0%,transparent 50%);pointer-events:none}
.wrap{position:relative;z-index:1;display:grid;grid-template-columns:1fr 1fr;max-width:940px;width:100%;background:var(--s1);border:1px solid var(--bdr);border-radius:10px;overflow:hidden;box-shadow:0 24px 60px rgba(0,0,0,.7)}
/* LEFT PANEL */
.left{background:linear-gradient(160deg,#0c1525 0%,#0f1e35 100%);padding:52px 44px;display:flex;flex-direction:column;gap:32px;border-right:1px solid var(--bdr)}
.brand-wrap{display:flex;flex-direction:column;gap:14px}
.brand-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(201,168,76,.1);border:1px solid rgba(201,168,76,.25);border-radius:4px;padding:5px 12px;width:fit-content}
.brand-badge-dot{width:7px;height:7px;border-radius:50%;background:var(--gold)}
.brand-badge-txt{font-family:var(--fm);font-size:11px;font-weight:500;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}
.brand-name{font-size:32px;font-weight:700;color:var(--tx);letter-spacing:-.02em;line-height:1}
.brand-name span{color:var(--gold)}
.brand-desc{font-size:13px;color:var(--mu);line-height:1.7;font-weight:300}
.divider{height:1px;background:linear-gradient(90deg,var(--bdr),transparent)}
.feats{display:flex;flex-direction:column;gap:10px}
.feat{display:flex;align-items:center;gap:12px;font-size:13px;color:var(--dim);font-weight:400}
.feat-dot{width:5px;height:5px;border-radius:50%;background:var(--gold);flex-shrink:0;opacity:.7}
.stack{display:flex;flex-wrap:wrap;gap:6px;margin-top:auto}
.stack-badge{background:rgba(255,255,255,.04);border:1px solid var(--bdr2);color:var(--mu);padding:4px 10px;border-radius:4px;font-size:11px;font-family:var(--fm);letter-spacing:.03em}
/* RIGHT PANEL */
.right{padding:52px 44px;display:flex;align-items:center;justify-content:center}
.form-wrap{width:100%}
.form-title{font-size:20px;font-weight:600;color:var(--tx);margin-bottom:6px;letter-spacing:-.01em}
.form-sub{font-size:13px;color:var(--mu);margin-bottom:28px;font-weight:300}
.tabs{display:flex;border-bottom:1px solid var(--bdr);margin-bottom:28px}
.tab{flex:1;padding:10px 0;border:none;background:transparent;color:var(--mu);font-family:var(--ff);font-weight:500;font-size:13px;cursor:pointer;border-bottom:2px solid transparent;transition:all .2s;letter-spacing:.02em}
.tab.active{color:var(--gold);border-bottom-color:var(--gold)}
.pane{display:none;flex-direction:column;gap:16px}
.pane.active{display:flex}
.fg label{display:block;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--mu);margin-bottom:6px}
.fg input,.fg select{width:100%;padding:10px 13px;background:var(--s3);border:1px solid var(--bdr);border-radius:var(--rs);color:var(--tx);font-size:13px;font-family:var(--ff);outline:none;transition:border-color .2s}
.fg input:focus,.fg select:focus{border-color:var(--gold)}
.fg select option{background:var(--s1)}
.eye{position:relative}
.eye input{padding-right:40px;width:100%}
.eye-btn{position:absolute;right:11px;top:50%;transform:translateY(-50%);background:none;border:none;cursor:pointer;font-size:14px;color:var(--mu)}
.frow{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.hint-box{background:var(--s3);border:1px solid var(--bdr);border-left:3px solid var(--gold);border-radius:var(--rs);padding:10px 14px;font-size:12px;color:var(--mu);line-height:1.7;font-family:var(--fm)}
.hint-box strong{color:var(--gold)}
.sub-btn{width:100%;padding:12px;background:var(--gold);border:none;border-radius:var(--rs);color:#0b0f1a;font-family:var(--ff);font-weight:600;font-size:14px;cursor:pointer;transition:all .2s;letter-spacing:.02em;margin-top:4px}
.sub-btn:hover{background:var(--gold2);box-shadow:0 4px 20px rgba(201,168,76,.3)}
.msg{padding:9px 13px;border-radius:var(--rs);font-size:12px;margin-top:2px;display:none;font-weight:500}
.msg.err{background:rgba(224,85,85,.1);border:1px solid rgba(224,85,85,.3);color:var(--red);display:block}
.msg.ok{background:rgba(58,171,110,.1);border:1px solid rgba(58,171,110,.3);color:var(--grn);display:block}
@media(max-width:680px){.wrap{grid-template-columns:1fr}.left{display:none}.right{padding:36px 28px}}
</style>
</head>
<body>
<div class="wrap">
  <!-- LEFT -->
  <div class="left">
    <div class="brand-wrap">
      <div class="brand-badge">
        <div class="brand-badge-dot"></div>
        <div class="brand-badge-txt">Research Intelligence</div>
      </div>
      <div class="brand-name">Gap<span>Insight</span></div>
      <div class="brand-desc">An intelligent platform for detecting under-researched areas in academic literature using hybrid database architecture and TF-IDF analysis.</div>
    </div>
    <div class="divider"></div>
    <div class="feats">
      <div class="feat"><div class="feat-dot"></div><span>Topic gap scoring with multi-factor analysis</span></div>
      <div class="feat"><div class="feat-dot"></div><span>Full-text search across indexed research papers</span></div>
      <div class="feat"><div class="feat-dot"></div><span>Personalised research recommendations</span></div>
      <div class="feat"><div class="feat-dot"></div><span>Hybrid Oracle + MongoDB persistence layer</span></div>
      <div class="feat"><div class="feat-dot"></div><span>Bookmark management with activity logging</span></div>
    </div>
    <div class="stack">
      <span class="stack-badge">Oracle DB</span>
      <span class="stack-badge">MongoDB</span>
      <span class="stack-badge">TF-IDF</span>
      <span class="stack-badge">Python</span>
      <span class="stack-badge">Flask</span>
    </div>
  </div>
  <!-- RIGHT -->
  <div class="right">
    <div class="form-wrap">
      <div class="form-title">Welcome back</div>
      <div class="form-sub">Sign in to your GapInsight account</div>
      <div class="tabs">
        <button class="tab active" onclick="switchTab('login',this)">Sign In</button>
        <button class="tab" onclick="switchTab('register',this)">Register</button>
      </div>
      <!-- LOGIN -->
      <div id="loginPane" class="pane active">
        <div class="fg"><label>Email Address</label><input type="email" id="lEmail" placeholder="you@university.edu"/></div>
        <div class="fg"><label>Password</label>
          <div class="eye"><input type="password" id="lPass" placeholder="Enter your password"/>
            <button class="eye-btn" type="button" onclick="togglePwd('lPass',this)">👁</button>
          </div>
        </div>
        <div class="hint-box">Demo — Student: <strong>kashaf@uni.edu / kashaf123</strong><br>Demo — Researcher: <strong>shahid@uni.edu / shahid123</strong></div>
        <button class="sub-btn" id="loginBtn" onclick="doLogin()">Sign In</button>
        <div id="lMsg" class="msg"></div>
      </div>
      <!-- REGISTER -->
      <div id="registerPane" class="pane">
        <div class="frow">
          <div class="fg"><label>Full Name</label><input type="text" id="rName" placeholder="Your full name"/></div>
          <div class="fg"><label>Role</label><select id="rRole"><option value="Student">Student</option><option value="Researcher">Researcher</option></select></div>
        </div>
        <div class="fg"><label>Email Address</label><input type="email" id="rEmail" placeholder="you@university.edu"/></div>
        <div class="fg"><label>Password</label><input type="password" id="rPass" placeholder="Create a password"/></div>
        <div class="frow">
          <div class="fg"><label>University</label><input type="text" id="rUni" placeholder="FAST NUCES"/></div>
          <div class="fg"><label>Reg No.</label><input type="text" id="rReg" placeholder="FA24-BAI-001"/></div>
        </div>
        <div class="fg"><label>Research Interest</label><input type="text" id="rInt" placeholder="e.g. Machine Learning, NLP"/></div>
        <button class="sub-btn" id="registerBtn" onclick="doRegister()">Create Account</button>
        <div id="rMsg" class="msg"></div>
      </div>
    </div>
  </div>
</div>
<script>
function switchTab(t,btn){
  document.querySelectorAll('.tab').forEach(b=>b.classList.remove('active'));
  document.querySelectorAll('.pane').forEach(p=>p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(t+'Pane').classList.add('active');
  document.querySelector('.form-title').textContent = t==='login' ? 'Welcome back' : 'Create an account';
  document.querySelector('.form-sub').textContent   = t==='login' ? 'Sign in to your GapInsight account' : 'Register to begin exploring research gaps';
}
function togglePwd(id,btn){const el=document.getElementById(id);el.type=el.type==='password'?'text':'password';btn.textContent=el.type==='text'?'🙈':'👁';}
function showMsg(id,txt,type){const el=document.getElementById(id);el.textContent=txt;el.className='msg '+type;setTimeout(()=>el.className='msg',4500);}
async function doLogin(){
  const email=document.getElementById('lEmail').value.trim();
  const password=document.getElementById('lPass').value;
  if(!email||!password){showMsg('lMsg','Please enter your email and password.','err');return;}
  const btn=document.getElementById('loginBtn');
  btn.textContent='Verifying…'; btn.disabled=true;
  try{
    const r=await fetch('/api/login',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,password})});
    const d=await r.json();
    if(d.success){showMsg('lMsg','Authentication successful. Redirecting…','ok');localStorage.setItem('gi_user',JSON.stringify(d.user));setTimeout(()=>window.location.href='/app',800);}
    else showMsg('lMsg',d.error||'Invalid credentials. Please try again.','err');
  }catch(e){showMsg('lMsg','Connection error: '+e.message,'err');}
  btn.textContent='Sign In'; btn.disabled=false;
}
async function doRegister(){
  const name=document.getElementById('rName').value.trim();
  const email=document.getElementById('rEmail').value.trim();
  const password=document.getElementById('rPass').value;
  const role=document.getElementById('rRole').value;
  const university=document.getElementById('rUni').value.trim();
  const research_interest=document.getElementById('rInt').value.trim();
  if(!name||!email||!password){showMsg('rMsg','Name, email and password are required.','err');return;}
  const btn=document.getElementById('registerBtn');
  btn.textContent='Creating account…'; btn.disabled=true;
  try{
    const r=await fetch('/api/register',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,email,password,role,university,research_interest})});
    const d=await r.json();
    if(d.success){showMsg('rMsg','Account created successfully. Please sign in.','ok');switchTab('login',document.querySelectorAll('.tab')[0]);document.getElementById('lEmail').value=email;}
    else showMsg('rMsg',d.error||'Registration failed.','err');
  }catch(e){showMsg('rMsg','Connection error: '+e.message,'err');}
  btn.textContent='Create Account'; btn.disabled=false;
}
document.addEventListener('keydown',e=>{if(e.key==='Enter'){const p=document.querySelector('.pane.active');p.id==='loginPane'?doLogin():doRegister();}});
</script>
</body>
</html>"""

# =============================================================================
#  MAIN APP PAGE — PROFESSIONAL SLATE + GOLD THEME
# =============================================================================
MAIN_APP_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>GapInsight — Research Analyzer</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --bg:#0b0f1a;--s1:#111827;--s2:#1a2235;--s3:#0e1520;--s4:#0d1828;
  --bdr:#1e2d42;--bdr2:#2a3d58;
  --tx:#e8eef6;--mu:#6b80a0;--dim:#94a8c4;
  --gold:#c9a84c;--gold2:#e8c76a;--gold3:#a07830;
  --blue:#3b7dd8;--red:#e05555;--grn:#3aab6e;--am:#d4883a;
  --ff:'IBM Plex Sans',sans-serif;--fm:'IBM Plex Mono',monospace;
  --sw:252px;--r:8px;--rs:5px
}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--tx);font-family:var(--ff);font-size:14px;line-height:1.6;overflow-x:hidden;letter-spacing:.01em}
a{color:inherit;text-decoration:none}
button{font-family:var(--ff);cursor:pointer}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--bdr2);border-radius:3px}

/* ── SIDEBAR ────────────────────── */
.sidebar{position:fixed;top:0;left:0;bottom:0;width:var(--sw);background:var(--s4);border-right:1px solid var(--bdr);display:flex;flex-direction:column;z-index:100;transition:transform .25s}
.sb-head{padding:22px 20px 18px;border-bottom:1px solid var(--bdr)}
.sb-logo{display:flex;align-items:center;gap:10px;margin-bottom:10px}
.sb-icon{width:34px;height:34px;background:rgba(201,168,76,.12);border:1px solid rgba(201,168,76,.25);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:16px}
.sb-name{font-size:15px;font-weight:700;color:var(--tx);letter-spacing:-.01em}
.sb-name span{color:var(--gold)}
.sb-ver{font-family:var(--fm);font-size:10px;color:var(--mu);letter-spacing:.06em}
.sb-nav{flex:1;padding:12px 10px;display:flex;flex-direction:column;gap:1px;overflow-y:auto}
.nav{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:var(--rs);color:var(--mu);font-size:13px;font-weight:500;transition:all .18s;border:1px solid transparent;cursor:pointer;background:none;width:100%;text-align:left}
.nav:hover{background:rgba(255,255,255,.04);color:var(--dim)}
.nav.active{background:rgba(201,168,76,.1);color:var(--gold);border-color:rgba(201,168,76,.2)}
.nav-ic{font-size:14px;width:18px;text-align:center;opacity:.8}
.sb-divider{height:1px;background:var(--bdr);margin:8px 10px}
.sb-foot{padding:12px 10px;border-top:1px solid var(--bdr)}
.u-chip{display:flex;align-items:center;gap:10px;padding:10px;background:rgba(255,255,255,.03);border:1px solid var(--bdr);border-radius:var(--rs);margin-bottom:8px}
.u-av{width:32px;height:32px;background:linear-gradient(135deg,var(--gold3),var(--gold));border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;color:#0b0f1a;flex-shrink:0}
.u-name{font-size:12px;font-weight:600;color:var(--tx)}
.u-role{font-size:11px;color:var(--mu)}
.logout{display:block;text-align:center;padding:8px;background:transparent;border:1px solid var(--bdr);border-radius:var(--rs);color:var(--mu);font-size:12px;font-weight:500;cursor:pointer;width:100%;transition:all .18s;letter-spacing:.02em}
.logout:hover{border-color:var(--red);color:var(--red)}

/* ── MAIN ───────────────────────── */
.main{margin-left:var(--sw);min-height:100vh;display:flex;flex-direction:column}
.topbar{display:flex;align-items:center;gap:16px;padding:0 28px;height:56px;background:var(--s1);border-bottom:1px solid var(--bdr);position:sticky;top:0;z-index:50}
.menu-btn{display:none;background:none;border:none;color:var(--mu);font-size:20px}
.tb-breadcrumb{display:flex;align-items:center;gap:8px;flex:1}
.tb-parent{font-size:12px;color:var(--mu);font-weight:500}
.tb-sep{font-size:12px;color:var(--bdr2)}
.tb-title{font-size:13px;font-weight:600;color:var(--tx)}
.tb-right{display:flex;align-items:center;gap:14px}
.status-pill{display:flex;align-items:center;gap:6px;background:rgba(58,171,110,.1);border:1px solid rgba(58,171,110,.2);border-radius:999px;padding:4px 10px}
.status-dot{width:6px;height:6px;border-radius:50%;background:var(--grn)}
.status-txt{font-family:var(--fm);font-size:11px;color:var(--grn)}
.pb{padding:28px;flex:1}

/* ── SECTION ─────────────────────── */
.section{display:none;animation:fadeIn .25s ease}
.section.active{display:block}
@keyframes fadeIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}

/* ── PAGE HEADER ────────────────── */
.ph{display:flex;align-items:center;justify-content:space-between;margin-bottom:24px;flex-wrap:wrap;gap:12px;padding-bottom:20px;border-bottom:1px solid var(--bdr)}
.ph-left{}
.ph-h2{font-size:20px;font-weight:600;color:var(--tx);letter-spacing:-.02em}
.ph-sub{color:var(--mu);font-size:13px;margin-top:3px;font-weight:300}

/* ── BUTTONS ─────────────────────── */
.btn-gold{padding:9px 20px;background:var(--gold);border:none;border-radius:var(--rs);color:#0b0f1a;font-family:var(--ff);font-weight:600;font-size:13px;cursor:pointer;transition:all .2s;display:inline-flex;align-items:center;gap:7px;letter-spacing:.01em}
.btn-gold:hover{background:var(--gold2);box-shadow:0 3px 16px rgba(201,168,76,.3)}
.btn-gold:disabled{opacity:.5;cursor:not-allowed}
.btn-outline{padding:8px 18px;background:transparent;border:1px solid var(--bdr2);border-radius:var(--rs);color:var(--dim);font-weight:500;font-size:13px;transition:all .2s;cursor:pointer}
.btn-outline:hover{border-color:var(--gold);color:var(--gold)}
.btn-danger{padding:6px 12px;background:transparent;border:1px solid rgba(224,85,85,.3);border-radius:var(--rs);color:var(--red);font-size:12px;font-weight:500;cursor:pointer;transition:all .18s}
.btn-danger:hover{background:rgba(224,85,85,.1)}

/* ── CARDS ───────────────────────── */
.card{background:var(--s1);border:1px solid var(--bdr);border-radius:var(--r);padding:22px;margin-bottom:18px}
.card-h{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid var(--bdr)}
.card-t{font-size:13px;font-weight:600;color:var(--tx);letter-spacing:.02em}
.card-sub{font-size:12px;color:var(--mu)}

/* ── STATS GRID ─────────────────── */
.sg{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:22px}
.sc{background:var(--s1);border:1px solid var(--bdr);border-radius:var(--r);padding:18px 20px;display:flex;align-items:center;gap:14px;transition:border-color .2s}
.sc:hover{border-color:var(--bdr2)}
.si{width:42px;height:42px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
.sn{font-size:24px;font-weight:700;line-height:1;color:var(--tx);font-family:var(--fm)}
.sl{font-size:11px;color:var(--mu);text-transform:uppercase;letter-spacing:.07em;margin-top:4px;font-weight:500}

/* ── SEARCH ──────────────────────── */
.search-row{display:flex;gap:10px;margin-bottom:14px}
.search-inp{flex:1;padding:11px 16px;background:var(--s3);border:1px solid var(--bdr);border-radius:var(--rs);color:var(--tx);font-size:14px;outline:none;font-family:var(--ff);transition:border-color .2s;letter-spacing:.01em}
.search-inp:focus{border-color:var(--gold)}
.search-inp::placeholder{color:var(--mu)}
.quick{display:flex;gap:7px;flex-wrap:wrap;margin-bottom:22px;align-items:center}
.quick-lbl{font-size:11px;color:var(--mu);font-weight:600;text-transform:uppercase;letter-spacing:.07em}
.qt{padding:5px 14px;background:transparent;border:1px solid var(--bdr);border-radius:999px;color:var(--mu);font-size:12px;font-weight:500;cursor:pointer;transition:all .18s}
.qt:hover{border-color:var(--gold);color:var(--gold)}

/* ── RESULT ──────────────────────── */
.result-wrap{animation:fadeIn .3s ease}
.status-card{border-radius:var(--r);padding:20px 24px;margin-bottom:18px;display:flex;align-items:flex-start;gap:16px;border:1px solid}
.status-card.critical{background:rgba(58,171,110,.06);border-color:rgba(58,171,110,.25)}
.status-card.high{background:rgba(201,168,76,.06);border-color:rgba(201,168,76,.25)}
.status-card.moderate{background:rgba(212,136,58,.06);border-color:rgba(212,136,58,.25)}
.status-card.low{background:rgba(224,85,85,.06);border-color:rgba(224,85,85,.2)}
.status-card.saturated{background:rgba(107,128,160,.06);border-color:rgba(107,128,160,.2)}
.status-icon-wrap{width:44px;height:44px;border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
.status-card.critical .status-icon-wrap{background:rgba(58,171,110,.12)}
.status-card.high .status-icon-wrap{background:rgba(201,168,76,.12)}
.status-card.moderate .status-icon-wrap{background:rgba(212,136,58,.12)}
.status-card.low .status-icon-wrap{background:rgba(224,85,85,.12)}
.status-card.saturated .status-icon-wrap{background:rgba(107,128,160,.12)}
.status-title{font-size:16px;font-weight:600;margin-bottom:4px}
.status-card.critical .status-title{color:#3aab6e}
.status-card.high .status-title{color:var(--gold)}
.status-card.moderate .status-title{color:var(--am)}
.status-card.low .status-title{color:var(--red)}
.status-card.saturated .status-title{color:var(--mu)}
.status-desc{font-size:13px;color:var(--dim);font-weight:300}
.score-section{margin:16px 0}
.score-header{display:flex;justify-content:space-between;font-size:12px;color:var(--mu);margin-bottom:7px;font-weight:500}
.score-track{height:8px;background:var(--s3);border-radius:4px;overflow:hidden;border:1px solid var(--bdr)}
.score-fill{height:100%;border-radius:4px;transition:width 1.2s cubic-bezier(.4,0,.2,1)}
.result-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px}
.rg-box{background:var(--s3);border:1px solid var(--bdr);border-radius:var(--rs);padding:14px 16px;text-align:center}
.rg-val{font-family:var(--fm);font-size:20px;font-weight:700;color:var(--tx)}
.rg-lbl{font-size:11px;color:var(--mu);margin-top:4px;text-transform:uppercase;letter-spacing:.07em;font-weight:500}

/* ── TABLE ───────────────────────── */
.papers-section-title{font-size:13px;font-weight:600;color:var(--tx);margin:20px 0 12px;padding-bottom:10px;border-bottom:1px solid var(--bdr);letter-spacing:.02em}
.paper-table{width:100%;border-collapse:collapse}
.paper-table th{padding:9px 14px;text-align:left;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.07em;color:var(--mu);background:var(--s3);border-bottom:1px solid var(--bdr);white-space:nowrap}
.paper-table td{padding:12px 14px;border-bottom:1px solid var(--bdr);font-size:13px;vertical-align:top}
.paper-table tr:last-child td{border-bottom:none}
.paper-table tr:hover td{background:rgba(255,255,255,.015)}
.paper-title-cell{font-weight:500;color:var(--tx);line-height:1.4}
.paper-abs-cell{font-size:12px;color:var(--mu);font-weight:300;max-width:300px}
.paper-year-cell{font-family:var(--fm);font-size:12px;color:var(--dim);white-space:nowrap}
.paper-cite-cell{font-family:var(--fm);font-size:12px;color:var(--mu);white-space:nowrap}
.bm-btn{padding:5px 12px;background:transparent;border:1px solid var(--bdr);border-radius:var(--rs);color:var(--mu);font-size:11px;font-weight:500;cursor:pointer;transition:all .18s;white-space:nowrap}
.bm-btn:hover,.bm-btn.saved{border-color:var(--gold);color:var(--gold);background:rgba(201,168,76,.08)}

/* ── CATEGORY BADGES ─────────────── */
.cat-badge{display:inline-block;padding:2px 8px;border-radius:3px;font-size:11px;font-weight:500;font-family:var(--fm);white-space:nowrap;border:1px solid}
.cat-nlp{background:rgba(59,125,216,.1);color:#6ba3e8;border-color:rgba(59,125,216,.25)}
.cat-ml{background:rgba(201,168,76,.1);color:var(--gold);border-color:rgba(201,168,76,.25)}
.cat-cv{background:rgba(212,136,58,.1);color:#e8a060;border-color:rgba(212,136,58,.25)}
.cat-dl{background:rgba(167,139,250,.1);color:#c4b0f8;border-color:rgba(167,139,250,.25)}
.cat-health{background:rgba(58,171,110,.1);color:#72d4a0;border-color:rgba(58,171,110,.25)}
.cat-default{background:rgba(107,128,160,.1);color:var(--dim);border-color:rgba(107,128,160,.2)}

/* ── GAP CARDS ───────────────────── */
.gaps-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.gap-card{background:var(--s1);border:1px solid var(--bdr);border-radius:var(--r);padding:18px;transition:border-color .2s}
.gap-card:hover{border-color:var(--bdr2)}
.gc-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.gc-badge{padding:2px 9px;border-radius:3px;font-size:10px;font-weight:600;font-family:var(--fm);border:1px solid;letter-spacing:.04em}
.gc-kw{font-size:15px;font-weight:600;color:var(--tx);margin-bottom:4px;letter-spacing:-.01em}
.gc-meta{font-size:12px;color:var(--mu);margin-bottom:12px;font-weight:300}
.gp-track{height:5px;background:var(--s3);border-radius:3px;overflow:hidden;margin-bottom:10px;border:1px solid var(--bdr)}
.gp-fill{height:100%;border-radius:3px;transition:width .8s ease}
.gc-foot{display:flex;justify-content:space-between;align-items:center}
.gc-trend{font-size:12px;color:var(--mu)}
.gc-score{font-family:var(--fm);font-size:13px;font-weight:600}

/* ── LIST ITEMS ──────────────────── */
.list-item{background:var(--s1);border:1px solid var(--bdr);border-radius:var(--rs);padding:14px 18px;margin-bottom:8px;display:flex;align-items:center;gap:14px;transition:border-color .2s}
.list-item:hover{border-color:var(--bdr2)}
.li-icon{font-size:18px;flex-shrink:0;width:32px;height:32px;background:var(--s3);border:1px solid var(--bdr);border-radius:6px;display:flex;align-items:center;justify-content:center}
.li-body{flex:1;min-width:0}
.li-title{font-weight:500;font-size:13px;color:var(--tx);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.li-sub{font-size:12px;color:var(--mu);margin-top:2px;font-weight:300}
.li-right{flex-shrink:0;text-align:right}
.li-time{font-family:var(--fm);font-size:11px;color:var(--mu)}

/* ── LOADER ──────────────────────── */
.loader{text-align:center;padding:48px 20px}
.spinner{width:36px;height:36px;border:2px solid rgba(201,168,76,.15);border-top-color:var(--gold);border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 14px}
@keyframes spin{to{transform:rotate(360deg)}}
.loader-txt{font-size:13px;color:var(--mu);font-weight:300}

/* ── ALERTS ──────────────────────── */
.alert{padding:10px 14px;border-radius:var(--rs);font-size:13px;margin-bottom:12px;font-weight:400}
.alert-err{background:rgba(224,85,85,.08);border:1px solid rgba(224,85,85,.25);color:var(--red);border-left:3px solid var(--red)}
.alert-ok{background:rgba(58,171,110,.08);border:1px solid rgba(58,171,110,.25);color:var(--grn);border-left:3px solid var(--grn)}

/* ── EMPTY ───────────────────────── */
.empty{text-align:center;padding:56px 20px}
.empty-ic{font-size:40px;margin-bottom:12px;opacity:.6}
.empty-t{font-size:16px;font-weight:600;color:var(--tx);margin-bottom:6px}
.empty-s{font-size:13px;color:var(--mu);font-weight:300}

/* ── TOAST ───────────────────────── */
#toast{position:fixed;bottom:24px;right:24px;z-index:999;padding:11px 16px;border-radius:var(--rs);font-size:13px;font-weight:500;display:none;box-shadow:0 8px 24px rgba(0,0,0,.5)}
#toast.ok{background:var(--s2);border:1px solid rgba(58,171,110,.3);border-left:3px solid var(--grn);color:var(--grn)}
#toast.err{background:var(--s2);border:1px solid rgba(224,85,85,.3);border-left:3px solid var(--red);color:var(--red)}

/* ── RECOMMEND BOX ───────────────── */
.rec-box{background:rgba(201,168,76,.04);border:1px solid rgba(201,168,76,.15);border-left:3px solid var(--gold);border-radius:var(--r);padding:16px 20px;margin-top:16px}
.rec-box-title{font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--gold);margin-bottom:8px}
.rec-box-text{font-size:13px;color:var(--dim);line-height:1.7;font-weight:300}

/* ── RESPONSIVE ──────────────────── */
@media(max-width:900px){.sidebar{transform:translateX(-100%)}.sidebar.open{transform:translateX(0)}.main{margin-left:0}.menu-btn{display:block}.sg{grid-template-columns:1fr 1fr}.result-grid{grid-template-columns:1fr 1fr}.paper-abs-cell{display:none}}
@media(max-width:500px){.sg,.result-grid{grid-template-columns:1fr}.pb{padding:16px}}
</style>
</head>
<body>

<!-- SIDEBAR -->
<aside class="sidebar" id="sidebar">
  <div class="sb-head">
    <div class="sb-logo">
      <div class="sb-icon">🔬</div>
      <div>
        <div class="sb-name">Gap<span>Insight</span></div>
        <div class="sb-ver">RESEARCH INTELLIGENCE v1.0</div>
      </div>
    </div>
  </div>
  <nav class="sb-nav">
    <button class="nav active" onclick="showSection('analyze',this)"><span class="nav-ic">🔍</span> Topic Analysis</button>
    <button class="nav" onclick="showSection('gaps',this)"><span class="nav-ic">📊</span> Research Gaps</button>
    <button class="nav" onclick="showSection('bookmarks',this)"><span class="nav-ic">🔖</span> Bookmarks</button>
    <button class="nav" onclick="showSection('history',this)"><span class="nav-ic">📋</span> Search History</button>
    <div class="sb-divider"></div>
    <button class="nav" onclick="showSection('dashboard',this)"><span class="nav-ic">📈</span> Dashboard</button>
  </nav>
  <div class="sb-foot">
    <div class="u-chip">
      <div class="u-av" id="uAv">G</div>
      <div><div class="u-name" id="uName">User</div><div class="u-role" id="uRole">Student</div></div>
    </div>
    <button class="logout" onclick="doLogout()">Sign Out</button>
  </div>
</aside>

<!-- MAIN -->
<main class="main">
  <div class="topbar">
    <button class="menu-btn" onclick="document.getElementById('sidebar').classList.toggle('open')">☰</button>
    <div class="tb-breadcrumb">
      <span class="tb-parent">GapInsight</span>
      <span class="tb-sep">›</span>
      <span class="tb-title" id="tbTitle">Topic Analysis</span>
    </div>
    <div class="tb-right">
      <div class="status-pill">
        <div class="status-dot"></div>
        <div class="status-txt">ONLINE</div>
      </div>
      <span style="font-size:12px;color:var(--mu);font-weight:500" id="tbUser">—</span>
    </div>
  </div>

  <div class="pb">

    <!-- ANALYZE -->
    <div id="analyzeSection" class="section active">
      <div class="ph">
        <div class="ph-left">
          <div class="ph-h2">Topic Analysis</div>
          <div class="ph-sub">Enter a research topic to evaluate its coverage and identify gaps in the literature</div>
        </div>
      </div>
      <div class="card">
        <div class="card-h"><span class="card-t">SEARCH</span><span class="card-sub">Full-text search across indexed papers</span></div>
        <div class="search-row">
          <input id="topicInput" class="search-inp" placeholder="e.g.  Urdu Natural Language Processing, TinyML, Federated Learning Privacy…" onkeydown="if(event.key==='Enter')doAnalyze()"/>
          <button class="btn-gold" id="analyzeBtn" onclick="doAnalyze()">Analyze</button>
        </div>
        <div class="quick">
          <span class="quick-lbl">Suggested</span>
          <button class="qt" onclick="setTopic('Federated Learning')">Federated Learning</button>
          <button class="qt" onclick="setTopic('Urdu NLP')">Urdu NLP</button>
          <button class="qt" onclick="setTopic('TinyML')">TinyML</button>
          <button class="qt" onclick="setTopic('Transformer')">Transformer</button>
          <button class="qt" onclick="setTopic('Deepfake Detection')">Deepfake Detection</button>
          <button class="qt" onclick="setTopic('3D Medical Imaging')">3D Medical Imaging</button>
        </div>
        <div id="analyzeResult"></div>
      </div>
    </div>

    <!-- GAPS -->
    <div id="gapsSection" class="section">
      <div class="ph">
        <div class="ph-left"><div class="ph-h2">Research Gaps</div><div class="ph-sub">Detected under-researched areas across the indexed knowledge base</div></div>
        <button class="btn-gold" onclick="runGapDetection()">Refresh Analysis</button>
      </div>
      <div id="gapsContent"><div class="loader"><div class="spinner"></div><div class="loader-txt">Loading research gaps…</div></div></div>
    </div>

    <!-- BOOKMARKS -->
    <div id="bookmarksSection" class="section">
      <div class="ph">
        <div class="ph-left"><div class="ph-h2">Bookmarks</div><div class="ph-sub">Papers saved to your personal reading list</div></div>
      </div>
      <div id="bookmarksContent"><div class="loader"><div class="spinner"></div><div class="loader-txt">Loading bookmarks…</div></div></div>
    </div>

    <!-- HISTORY -->
    <div id="historySection" class="section">
      <div class="ph">
        <div class="ph-left"><div class="ph-h2">Search History</div><div class="ph-sub">Your recent topic analysis queries</div></div>
      </div>
      <div id="historyContent"><div class="loader"><div class="spinner"></div><div class="loader-txt">Loading history…</div></div></div>
    </div>

    <!-- DASHBOARD -->
    <div id="dashboardSection" class="section">
      <div class="ph">
        <div class="ph-left"><div class="ph-h2">Dashboard</div><div class="ph-sub">System statistics and knowledge base overview</div></div>
      </div>
      <div id="statsGrid" class="sg"></div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">
        <div class="card"><div class="card-h"><span class="card-t">PAPERS BY CATEGORY</span></div><div style="max-height:260px;display:flex;align-items:center;justify-content:center"><canvas id="catChart"></canvas></div></div>
        <div class="card"><div class="card-h"><span class="card-t">TOP RESEARCH GAPS</span></div><canvas id="gapChart" style="max-height:260px"></canvas></div>
      </div>
    </div>

  </div>
</main>

<div id="toast"></div>

<script>
// ── State ─────────────────────────────────────────────────────────────────────
let currentUser=null, bookmarkedIds=new Set(), catChartInst=null, gapChartInst=null;
const sectionTitles={analyze:'Topic Analysis',gaps:'Research Gaps',bookmarks:'Bookmarks',history:'Search History',dashboard:'Dashboard'};

(function init(){
  const s=localStorage.getItem('gi_user');
  if(!s){window.location.href='/';return;}
  try{currentUser=JSON.parse(s);}catch(e){window.location.href='/';return;}
  document.getElementById('uAv').textContent=(currentUser.name||'G')[0].toUpperCase();
  document.getElementById('uName').textContent=currentUser.name||'User';
  document.getElementById('uRole').textContent=currentUser.role||'Student';
  document.getElementById('tbUser').textContent=currentUser.name||'—';
  loadBookmarkIds();
})();

function showSection(name,btn){
  document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));
  document.querySelectorAll('.nav').forEach(b=>b.classList.remove('active'));
  document.getElementById(name+'Section').classList.add('active');
  if(btn)btn.classList.add('active');
  document.getElementById('tbTitle').textContent=sectionTitles[name]||name;
  if(name==='gaps')      loadGaps();
  if(name==='bookmarks') loadBookmarks();
  if(name==='history')   loadHistory();
  if(name==='dashboard') loadDashboard();
  document.getElementById('sidebar').classList.remove('open');
}

// ── ANALYZE ───────────────────────────────────────────────────────────────────
function setTopic(t){document.getElementById('topicInput').value=t;doAnalyze();}

function gapColor(s){
  if(s>=0.7)return'#3aab6e';
  if(s>=0.5)return'#c9a84c';
  if(s>=0.3)return'#d4883a';
  return'#e05555';
}

async function doAnalyze(){
  const topic=document.getElementById('topicInput').value.trim();
  if(!topic){showToast('Please enter a research topic.','err');return;}
  const btn=document.getElementById('analyzeBtn');
  btn.disabled=true;btn.textContent='Analysing…';
  document.getElementById('analyzeResult').innerHTML='<div class="loader"><div class="spinner"></div><div class="loader-txt">Searching literature and computing gap score…</div></div>';
  try{
    const r=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({topic})});
    const d=await r.json();
    if(d.success)renderResult(d.result);
    else document.getElementById('analyzeResult').innerHTML=`<div class="alert alert-err">${d.error||'An error occurred during analysis.'}</div>`;
  }catch(e){document.getElementById('analyzeResult').innerHTML=`<div class="alert alert-err">Connection error: ${e.message}</div>`;}
  btn.disabled=false;btn.textContent='Analyze';
}

function renderResult(res){
  const pct=Math.round(res.gap_score*100);
  const col=gapColor(res.gap_score);
  const icons={critical:'🟢',high:'🟡',moderate:'🟠',low:'🔴',saturated:'⬛'};
  let html=`<div class="result-wrap">
  <div class="status-card ${res.color}">
    <div class="status-icon-wrap">${icons[res.color]||'📊'}</div>
    <div>
      <div class="status-title">${esc(res.status_text)}</div>
      <div class="status-desc">${esc(res.status_desc)}</div>
    </div>
  </div>
  <div class="result-grid">
    <div class="rg-box"><div class="rg-val" style="color:${col}">${pct}%</div><div class="rg-lbl">Gap Score</div></div>
    <div class="rg-box"><div class="rg-val" style="color:var(--tx)">${res.paper_count}</div><div class="rg-lbl">Related Papers</div></div>
    <div class="rg-box"><div class="rg-val" style="color:var(--gold)">${res.total_papers_in_db||0}</div><div class="rg-lbl">Total Indexed</div></div>
    <div class="rg-box"><div class="rg-val" style="color:var(--dim)">${res.gap_score>=0.7?'High':res.gap_score>=0.4?'Medium':'Low'}</div><div class="rg-lbl">Opportunity</div></div>
  </div>
  <div class="score-section">
    <div class="score-header"><span>Research Gap Score — higher indicates a less-covered area</span><span style="font-family:var(--fm);font-weight:600;color:${col}">${pct} / 100</span></div>
    <div class="score-track"><div class="score-fill" style="width:${pct}%;background:${col}"></div></div>
  </div>`;

  if(res.related_papers&&res.related_papers.length>0){
    html+=`<div class="papers-section-title">RELATED PAPERS &nbsp;<span style="font-weight:400;color:var(--mu);font-family:var(--fm)">(${res.related_papers.length} found)</span></div>
    <div style="overflow-x:auto"><table class="paper-table">
    <thead><tr><th>Title</th><th>Category</th><th>Year</th><th>Citations</th><th>Abstract</th><th></th></tr></thead><tbody>`;
    for(const p of res.related_papers){
      const saved=bookmarkedIds.has(p.id);
      html+=`<tr>
        <td class="paper-title-cell" style="max-width:220px">${esc(p.title)}</td>
        <td><span class="cat-badge ${catClass(p.category)}">${esc(p.category)}</span></td>
        <td class="paper-year-cell">${p.year}</td>
        <td class="paper-cite-cell">${(p.citation_count||0).toLocaleString()}</td>
        <td class="paper-abs-cell">${esc(p.abstract.substring(0,100))}…</td>
        <td><button class="bm-btn ${saved?'saved':''}" id="bm-${p.id}" onclick="toggleBookmark('${p.id}','${esc(p.title)}','${esc(p.abstract)}','${esc(p.category)}',${p.year})">${saved?'★ Saved':'☆ Save'}</button></td>
      </tr>`;
    }
    html+=`</tbody></table></div>`;
  }else{
    html+=`<div style="text-align:center;padding:28px;background:var(--s3);border:1px solid var(--bdr);border-radius:var(--r);margin-top:8px">
      <div style="font-size:13px;font-weight:600;color:var(--tx);margin-bottom:6px">No existing papers found</div>
      <div style="font-size:13px;color:var(--mu);font-weight:300">This confirms a genuine research gap — foundational work in this area could have significant impact.</div>
    </div>`;
  }

  const tip=res.gap_score>=0.7
    ?'Excellent research opportunity. Very few papers exist in this area. Foundational work will have high citation potential and scholarly impact.'
    :res.gap_score>=0.4
    ?'Viable research opportunity. Some prior work exists. Focus on a specific unexplored sub-problem or underserved application domain.'
    :'Competitive research area. High publication volume detected. Consider novel interdisciplinary angles or specific methodological improvements.';

  html+=`<div class="rec-box"><div class="rec-box-title">Recommendation</div><div class="rec-box-text">${tip}</div></div></div>`;
  document.getElementById('analyzeResult').innerHTML=html;
}

// ── BOOKMARKS ─────────────────────────────────────────────────────────────────
async function loadBookmarkIds(){try{const r=await fetch('/api/bookmarks');const d=await r.json();if(d.success)d.bookmarks.forEach(b=>bookmarkedIds.add(b.paper_id));}catch(e){}}

async function toggleBookmark(id,title,abstract,category,year){
  const btn=document.getElementById('bm-'+id);
  const isSaved=bookmarkedIds.has(id);
  if(isSaved){
    try{const r=await fetch('/api/bookmark',{method:'DELETE',headers:{'Content-Type':'application/json'},body:JSON.stringify({paper_id:id})});const d=await r.json();if(d.success){bookmarkedIds.delete(id);if(btn){btn.textContent='☆ Save';btn.classList.remove('saved');}showToast('Bookmark removed.','ok');}}catch(e){showToast('Error removing bookmark.','err');}
  }else{
    try{const r=await fetch('/api/bookmark',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({paper_id:id,title,abstract,category,year})});const d=await r.json();if(d.success){bookmarkedIds.add(id);if(btn){btn.textContent='★ Saved';btn.classList.add('saved');}showToast('Paper saved to bookmarks.','ok');}}catch(e){showToast('Error saving bookmark.','err');}
  }
}

async function loadBookmarks(){
  const el=document.getElementById('bookmarksContent');
  el.innerHTML='<div class="loader"><div class="spinner"></div><div class="loader-txt">Loading bookmarks…</div></div>';
  try{
    const r=await fetch('/api/bookmarks');const d=await r.json();
    if(!d.success||d.bookmarks.length===0){el.innerHTML='<div class="empty"><div class="empty-ic">🔖</div><div class="empty-t">No bookmarks saved</div><div class="empty-s">Analyse topics and save papers to build your reading list.</div></div>';return;}
    let html='';
    for(const bm of d.bookmarks){
      html+=`<div class="list-item">
        <div class="li-icon">📄</div>
        <div class="li-body"><div class="li-title">${esc(bm.title||'Unknown Paper')}</div><div class="li-sub">${esc(bm.category||'General')} &nbsp;·&nbsp; ${bm.year||'N/A'}</div></div>
        <div class="li-right" style="display:flex;flex-direction:column;align-items:flex-end;gap:6px">
          <div class="li-time">${bm.saved_at||''}</div>
          <button class="btn-danger" onclick="removeBookmark('${bm.paper_id}')">Remove</button>
        </div>
      </div>`;
    }
    el.innerHTML=html;
  }catch(e){el.innerHTML=`<div class="alert alert-err">Error loading bookmarks: ${e.message}</div>`;}
}

async function removeBookmark(id){
  try{const r=await fetch('/api/bookmark',{method:'DELETE',headers:{'Content-Type':'application/json'},body:JSON.stringify({paper_id:id})});const d=await r.json();if(d.success){bookmarkedIds.delete(id);showToast('Bookmark removed.','ok');loadBookmarks();}}catch(e){showToast('Error removing bookmark.','err');}
}

// ── HISTORY ───────────────────────────────────────────────────────────────────
async function loadHistory(){
  const el=document.getElementById('historyContent');
  el.innerHTML='<div class="loader"><div class="spinner"></div><div class="loader-txt">Loading search history…</div></div>';
  try{
    const r=await fetch('/api/history');const d=await r.json();
    if(!d.success||d.history.length===0){el.innerHTML='<div class="empty"><div class="empty-ic">📋</div><div class="empty-t">No search history</div><div class="empty-s">Your topic analysis history will appear here.</div></div>';return;}
    let html='';
    for(const h of d.history){
      html+=`<div class="list-item" style="cursor:pointer" onclick="setTopicAndAnalyze('${esc(h.query)}')">
        <div class="li-icon">🔍</div>
        <div class="li-body"><div class="li-title">${esc(h.query)}</div><div class="li-sub">${h.results_count} related paper${h.results_count!==1?'s':''} found</div></div>
        <div class="li-right"><div class="li-time">${h.searched_at||''}</div></div>
      </div>`;
    }
    el.innerHTML=html;
  }catch(e){el.innerHTML=`<div class="alert alert-err">Error loading history: ${e.message}</div>`;}
}

function setTopicAndAnalyze(t){document.getElementById('topicInput').value=t;showSection('analyze',document.querySelector('.nav'));doAnalyze();}

// ── GAPS ──────────────────────────────────────────────────────────────────────
async function loadGaps(){
  const el=document.getElementById('gapsContent');
  el.innerHTML='<div class="loader"><div class="spinner"></div><div class="loader-txt">Loading research gaps…</div></div>';
  try{
    const r=await fetch('/api/gaps');const d=await r.json();
    if(!d.success||!d.gaps||d.gaps.length===0){el.innerHTML='<div class="empty"><div class="empty-ic">📊</div><div class="empty-t">No gaps detected</div><div class="empty-s">Click "Refresh Analysis" to run gap detection on all indexed papers.</div></div>';return;}
    let html='<div class="gaps-grid">';
    for(const g of d.gaps){
      const score=g.gap_score||0,pct=Math.round(score*100),col=gapColor(score);
      const label=score>=0.7?'Critical Gap':score>=0.5?'Significant':score>=0.3?'Moderate':'Well Covered';
      html+=`<div class="gap-card">
        <div class="gc-top">
          <span class="cat-badge ${catClass(g.category||'')}">${esc(g.category||'General')}</span>
          <span class="gc-badge" style="color:${col};border-color:${col}40;background:${col}12">${label}</span>
        </div>
        <div class="gc-kw">${esc(g.term||g.keyword||'')}</div>
        <div class="gc-meta">${g.frequency||0} paper${g.frequency!==1?'s':''} indexed for this topic</div>
        <div class="gp-track"><div class="gp-fill" style="width:${pct}%;background:${col}"></div></div>
        <div class="gc-foot">
          <span class="gc-trend">${g.trend==='rising'?'↑ Rising':g.trend==='declining'?'↓ Declining':'→ Stable'}</span>
          <span class="gc-score" style="color:${col}">${score.toFixed(4)}</span>
        </div>
      </div>`;
    }
    html+='</div>';
    el.innerHTML=html;
  }catch(e){el.innerHTML=`<div class="alert alert-err">Error: ${e.message}</div>`;}
}

async function runGapDetection(){
  const el=document.getElementById('gapsContent');
  el.innerHTML='<div class="loader"><div class="spinner"></div><div class="loader-txt">Running gap detection analysis across all indexed papers…</div></div>';
  try{
    const r=await fetch('/api/run_gap_detection',{method:'POST',headers:{'Content-Type':'application/json'}});
    const d=await r.json();
    if(d.success){showToast(d.message||'Analysis complete.','ok');loadGaps();}
    else el.innerHTML=`<div class="alert alert-err">Error: ${d.error}</div>`;
  }catch(e){el.innerHTML=`<div class="alert alert-err">Error: ${e.message}</div>`;}
}

// ── DASHBOARD ─────────────────────────────────────────────────────────────────
async function loadDashboard(){
  try{
    const r=await fetch('/api/stats');const d=await r.json();
    if(!d.success)return;
    const s=d.stats;
    document.getElementById('statsGrid').innerHTML=`
      <div class="sc"><div class="si" style="background:rgba(59,125,216,.12);color:#6ba3e8">📄</div><div><div class="sn">${s.total_papers||0}</div><div class="sl">Total Papers</div></div></div>
      <div class="sc"><div class="si" style="background:rgba(58,171,110,.12);color:#72d4a0">🔬</div><div><div class="sn">${s.total_gaps||0}</div><div class="sl">Research Gaps</div></div></div>
      <div class="sc"><div class="si" style="background:rgba(201,168,76,.12);color:var(--gold)">📂</div><div><div class="sn">${s.categories||0}</div><div class="sl">Categories</div></div></div>
      <div class="sc"><div class="si" style="background:rgba(212,136,58,.12);color:#e8a060">📈</div><div><div class="sn">${Math.round((s.top_gap_score||0)*100)}%</div><div class="sl">Top Gap Score</div></div></div>`;
    if(d.categories){
      const labels=Object.keys(d.categories),vals=Object.values(d.categories);
      const cols=['#3b7dd8','#3aab6e','#c9a84c','#d4883a','#e05555','#6ba3e8','#a78bfa','#72d4a0','#e8a060','#f472b6'];
      if(catChartInst)catChartInst.destroy();
      catChartInst=new Chart(document.getElementById('catChart'),{
        type:'doughnut',
        data:{labels,datasets:[{data:vals,backgroundColor:cols.slice(0,labels.length),borderWidth:2,borderColor:'#111827'}]},
        options:{responsive:true,maintainAspectRatio:true,plugins:{legend:{position:'right',labels:{color:'#6b80a0',font:{size:11,family:'IBM Plex Sans'},boxWidth:11}}}}
      });
    }
    if(d.top_gaps&&d.top_gaps.length>0){
      const gl=d.top_gaps.slice(0,8);
      const gLabels=gl.map(g=>(g.term||g.keyword||'').slice(0,22));
      const gScores=gl.map(g=>+(g.gap_score||0).toFixed(4));
      const gColors=gScores.map(s=>s>=0.6?'rgba(58,171,110,.7)':s>=0.4?'rgba(201,168,76,.7)':'rgba(224,85,85,.7)');
      if(gapChartInst)gapChartInst.destroy();
      gapChartInst=new Chart(document.getElementById('gapChart'),{
        type:'bar',
        data:{labels:gLabels,datasets:[{label:'Gap Score',data:gScores,backgroundColor:gColors,borderRadius:4,borderWidth:0}]},
        options:{responsive:true,indexAxis:'y',
          scales:{x:{min:0,max:1,grid:{color:'rgba(255,255,255,.04)'},ticks:{color:'#6b80a0',font:{size:10,family:'IBM Plex Mono'}}},
                  y:{grid:{color:'rgba(255,255,255,.03)'},ticks:{color:'#94a8c4',font:{size:11,family:'IBM Plex Sans'}}}},
          plugins:{legend:{display:false},tooltip:{callbacks:{label:c=>' Score: '+c.raw.toFixed(4)}}}}
      });
    }
  }catch(e){console.error('Dashboard error:',e);}
}

// ── HELPERS ───────────────────────────────────────────────────────────────────
function esc(t){if(!t)return'';const d=document.createElement('div');d.textContent=t;return d.innerHTML;}
function catClass(c){return({'Natural Language Processing':'cat-nlp','Machine Learning':'cat-ml','Computer Vision':'cat-cv','Deep Learning':'cat-dl','Healthcare AI':'cat-health'})[c]||'cat-default';}
function showToast(msg,type){const t=document.getElementById('toast');t.textContent=msg;t.className=type;t.style.display='block';clearTimeout(t._t);t._t=setTimeout(()=>t.style.display='none',3500);}
async function doLogout(){try{await fetch('/api/logout',{method:'POST'});}catch(e){}localStorage.removeItem('gi_user');window.location.href='/';}
</script>
</body>
</html>"""

# =============================================================================
#  API ROUTES  (unchanged from original)
# =============================================================================

@app.route('/')
def index():
    return LOGIN_PAGE

@app.route('/app')
def app_page():
    return MAIN_APP_PAGE

@app.route('/api/login', methods=['POST'])
def api_login():
    data=request.json or {}
    email=data.get('email',''); password=data.get('password','')
    if not ENGINE_AVAILABLE:
        demos={"kashaf@uni.edu":("kashaf123",{"user_id":1,"name":"Kashaf Fayyaz","email":"kashaf@uni.edu","role":"Student"}),
               "shahid@uni.edu":("shahid123",{"user_id":2,"name":"Dr. Shahid Ali","email":"shahid@uni.edu","role":"Researcher"}),
               "sara@uni.edu":   ("sara123",  {"user_id":3,"name":"Sara Ahmed","email":"sara@uni.edu","role":"Student"})}
        if email in demos and demos[email][0]==password:
            return jsonify({"success":True,"user":demos[email][1]})
        return jsonify({"success":False,"error":"Invalid credentials."})
    oracle,mongo=get_db_connections()
    if oracle is None: return jsonify({"success":False,"error":"Database connection failed."})
    user=login_user(oracle,email,password)
    if user: session['user_id']=user['user_id']; return jsonify({"success":True,"user":user})
    return jsonify({"success":False,"error":"Invalid credentials."})

@app.route('/api/register', methods=['POST'])
def api_register():
    data=request.json or {}
    try:
        if not ENGINE_AVAILABLE:
            return jsonify({"success":True,"user":{"name":data.get("name"),"email":data.get("email"),"role":data.get("role","Student")}})
        oracle,_=get_db_connections()
        if oracle is None: return jsonify({"success":False,"error":"Database connection failed."})
        user=register_user(oracle,name=data.get("name",""),email=data.get("email",""),
            password=data.get("password",""),role=data.get("role","Student"),
            university=data.get("university",""),research_interest=data.get("research_interest",""))
        return jsonify({"success":True,"user":user})
    except Exception as e: return jsonify({"success":False,"error":str(e)})

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear(); return jsonify({"success":True})

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data=request.json or {}; topic=data.get('topic','').strip()
    if not topic: return jsonify({"success":False,"error":"No topic provided."})
    _,mongo_conn=get_db_connections()
    analyzer=TopicAnalyzer(mongo_conn if ENGINE_AVAILABLE else None)
    result=analyzer.analyze_topic(topic)
    user_id=session.get('user_id')
    if user_id and mongo_conn:
        try: mongo_conn.log_search(user_id,topic,result['paper_count'])
        except: pass
    return jsonify({"success":True,"result":result})

@app.route('/api/stats', methods=['GET'])
def api_stats():
    _,mongo_conn=get_db_connections()
    if not mongo_conn or not ENGINE_AVAILABLE:
        return jsonify({"success":True,"stats":{"total_papers":len(DEMO_PAPERS),"categories":4,"total_gaps":0,"top_gap_score":0}})
    try:
        papers=mongo_conn.get_all_papers()
        cats={}
        for p in papers: c=p.get('category','Other'); cats[c]=cats.get(c,0)+1
        gaps=mongo_conn.get_top_gaps(limit=8)
        top_score=gaps[0]['gap_score'] if gaps else 0
        total_gaps=mongo_conn.db.keywords.count_documents({})
        top_gaps_data=[{"term":g.get('term',g.get('keyword','')),"gap_score":g.get('gap_score',0),"category":g.get('category','')} for g in gaps]
        return jsonify({"success":True,"stats":{"total_papers":len(papers),"categories":len(cats),"total_gaps":total_gaps,"top_gap_score":top_score},"categories":cats,"top_gaps":top_gaps_data})
    except: return jsonify({"success":True,"stats":{"total_papers":len(DEMO_PAPERS),"categories":4,"total_gaps":0,"top_gap_score":0}})

@app.route('/api/gaps', methods=['GET'])
def api_gaps():
    _,mongo_conn=get_db_connections()
    if not mongo_conn or not ENGINE_AVAILABLE: return jsonify({"success":True,"gaps":[]})
    try: return jsonify({"success":True,"gaps":mongo_conn.get_top_gaps(limit=60)})
    except: return jsonify({"success":True,"gaps":[]})

@app.route('/api/run_gap_detection', methods=['POST'])
def api_run_gap_detection():
    if not ENGINE_AVAILABLE: return jsonify({"success":False,"error":"Engine not available."})
    oracle_conn,mongo_conn=get_db_connections()
    if oracle_conn is None or mongo_conn is None: return jsonify({"success":False,"error":"Database connection failed."})
    try:
        mongo_conn.db.keywords.drop()
        detector=GapDetector(oracle_conn,mongo_conn)
        gaps=detector.analyze_and_detect()
        return jsonify({"success":True,"message":f"Analysis complete. {len(gaps)} research gaps identified.","gap_count":len(gaps)})
    except Exception as e:
        traceback.print_exc(); return jsonify({"success":False,"error":str(e)})

@app.route('/api/history', methods=['GET'])
def api_history():
    user_id=session.get('user_id')
    if not user_id or not ENGINE_AVAILABLE: return jsonify({"success":True,"history":[]})
    _,mongo_conn=get_db_connections()
    if not mongo_conn: return jsonify({"success":True,"history":[]})
    try:
        hist=list(mongo_conn.db.search_history.find({"user_id":user_id}).sort("searched_at",-1).limit(20))
        for h in hist:
            h['_id']=str(h['_id'])
            h['searched_at']=h['searched_at'].strftime('%Y-%m-%d %H:%M') if h.get('searched_at') else ''
        return jsonify({"success":True,"history":hist})
    except: return jsonify({"success":True,"history":[]})

@app.route('/api/bookmarks', methods=['GET'])
def api_get_bookmarks():
    user_id=session.get('user_id')
    if not user_id or not ENGINE_AVAILABLE: return jsonify({"success":True,"bookmarks":[]})
    oracle_conn,mongo_conn=get_db_connections()
    if not oracle_conn: return jsonify({"success":True,"bookmarks":[]})
    try:
        bms=oracle_conn.get_bookmarks(user_id); enriched=[]
        for bm in bms:
            paper={}
            if bm.get('paper_id') and mongo_conn:
                try: paper=mongo_conn.get_paper(bm['paper_id']) or {}
                except: pass
            enriched.append({"paper_id":bm['paper_id'],
                "saved_at":bm['saved_at'].strftime('%Y-%m-%d %H:%M') if bm.get('saved_at') else '',
                "title":paper.get('title','Unknown Paper'),"category":paper.get('category','General'),"year":paper.get('year','N/A')})
        return jsonify({"success":True,"bookmarks":enriched})
    except: return jsonify({"success":True,"bookmarks":[]})

@app.route('/api/bookmark', methods=['POST','DELETE'])
def api_bookmark():
    user_id=session.get('user_id')
    if not user_id: return jsonify({"success":False,"error":"Not logged in."})
    data=request.json or {}; paper_id=data.get('paper_id','')
    if not paper_id: return jsonify({"success":False,"error":"No paper ID provided."})
    if not ENGINE_AVAILABLE: return jsonify({"success":True,"action":"added" if request.method=='POST' else "removed"})
    oracle_conn,mongo_conn=get_db_connections()
    if not oracle_conn: return jsonify({"success":False,"error":"Database connection failed."})
    if request.method=='POST':
        if mongo_conn:
            try:
                if not mongo_conn.get_paper(paper_id):
                    mongo_conn.insert_paper({"title":data.get('title',''),"abstract":data.get('abstract',''),
                        "category":data.get('category',''),"year":data.get('year',2024),
                        "keywords":[],"citation_count":0,"uploaded_by_user_id":user_id,"status":"indexed"})
            except: pass
        ok=oracle_conn.add_bookmark(user_id,paper_id,f"Saved: {data.get('title','')[:60]}")
        return jsonify({"success":bool(ok),"action":"added"})
    else:
        try:
            oracle_conn.cursor.execute("DELETE FROM Bookmarks WHERE user_id=:1 AND paper_id=:2",[user_id,paper_id])
            oracle_conn.conn.commit(); return jsonify({"success":True,"action":"removed"})
        except Exception as e:
            oracle_conn.conn.rollback(); return jsonify({"success":False,"error":str(e)})

if __name__=='__main__':
    print("\n"+"="*60)
    print("  GapInsight — Research Gap Detection System")
    print("="*60)
    print("  URL    :  http://localhost:5000")
    print("  Accounts:")
    print("    kashaf@uni.edu  /  kashaf123   Student")
    print("    shahid@uni.edu  /  shahid123   Researcher")
    print("    sara@uni.edu    /  sara123     Student")
    print("="*60+"\n")
    app.run(debug=True,host='0.0.0.0',port=5000)