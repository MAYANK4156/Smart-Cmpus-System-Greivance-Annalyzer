"""AI module: category + priority prediction and duplicate detection.
Single entry point: analyze(text, existing). Loosely coupled to the web app."""
import os, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE = os.path.dirname(os.path.abspath(__file__))
try:
    _cat = joblib.load(os.path.join(BASE, "models", "category.pkl"))
    _pri = joblib.load(os.path.join(BASE, "models", "priority.pkl"))
except Exception:
    _cat = _pri = None          # fallback: app works without AI (manual / admin classification)

_enc = None
MODE, THRESHOLD = "tfidf-cosine", 0.60
if os.environ.get("USE_EMBEDDINGS") == "1":      # optional, off by default
    try:
        from sentence_transformers import SentenceTransformer, util
        _enc = SentenceTransformer("all-MiniLM-L6-v2")
        MODE, THRESHOLD = "sentence-embeddings", 0.75
    except Exception:
        _enc = None

def _find_duplicate(text, existing):
    if not existing:
        return None
    ids, texts = [i for i, _ in existing], [t for _, t in existing]
    if _enc is not None:
        scores = util.cos_sim(_enc.encode(text), _enc.encode(texts))[0].tolist()
    else:
        m = TfidfVectorizer(stop_words="english").fit(texts + [text])
        scores = cosine_similarity(m.transform([text]), m.transform(texts))[0].tolist()
    best = max(range(len(scores)), key=scores.__getitem__)
    return ids[best] if scores[best] >= THRESHOLD else None

def analyze(text, existing):
    """existing = list of (id, text). Returns (category, priority, duplicate_of_id)."""
    category = _cat.predict([text])[0] if _cat else "Unclassified"
    priority = _pri.predict([text])[0] if _pri else "Medium"
    return category, priority, _find_duplicate(text, existing)
