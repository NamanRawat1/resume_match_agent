# core/similarity.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils import normalize_text

def compute_tfidf_similarity(resume_text: str, job_text: str) -> float:
    """
    Returns similarity in range 0..1
    """
    r = normalize_text(resume_text)
    j = normalize_text(job_text)
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=20000)
    tfidf = vectorizer.fit_transform([r, j])
    if tfidf.shape[0] < 2:
        return 0.0
    sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return float(sim)
