# search.py - End-to-End live demo endpoint
# Input: any text or ISO control ID
# Output: NLP extraction + TF-IDF mapping + confidence score

from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import json
import os

router = APIRouter(prefix="/search", tags=["Live Search & Demo"])

nlp = spacy.load("en_core_web_sm")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIST_FILE = os.path.join(BASE_DIR, "mappings", "nist_csf_controls.json")
ISO_FILE = os.path.join(BASE_DIR, "mappings", "complete_iso_nist_mapping.json")

CONTROL_KEYWORDS = [
    "shall", "must", "should", "required", "mandatory",
    "ensure", "establish", "maintain", "implement", "document",
    "review", "monitor", "assess", "control", "protect",
    "define", "develop", "manage", "apply", "perform"
]

def load_nist():
    with open(NIST_FILE) as f:
        return json.load(f)["controls"]

def load_iso():
    with open(ISO_FILE) as f:
        return json.load(f)

def tfidf_match(text, nist_controls, top_n=3):
    nist_texts = [c["title"] for c in nist_controls]
    all_texts = [text] + nist_texts
    vec = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
    mat = vec.fit_transform(all_texts)
    sims = cosine_similarity(mat[0:1], mat[1:])[0]
    top_indices = sims.argsort()[::-1][:top_n]
    results = []
    for idx in top_indices:
        score = float(sims[idx])
        confidence = round(min(0.5 + score * 0.49, 0.99), 2)
        results.append({
            "nist_control_id": nist_controls[idx]["id"],
            "nist_control_title": nist_controls[idx]["title"],
            "nist_function": nist_controls[idx]["function"],
            "confidence_score": confidence,
            "confidence_percent": f"{round(confidence * 100, 1)}%",
            "match_strength": "High" if confidence >= 0.85 else "Medium" if confidence >= 0.70 else "Low"
        })
    return results

class SearchInput(BaseModel):
    query: str
    top_n: int = 3

@router.post("/map")
def live_map(body: SearchInput):
    """
    Core end-to-end demo endpoint.
    Input: any text (ISO control text, policy statement, etc.)
    Output: step-by-step NLP processing + top NIST CSF matches
    """
    query = body.query.strip()
    if not query:
        return {"error": "Query cannot be empty"}

    nist_controls = load_nist()

    # Step 1: NLP keyword detection
    query_lower = query.lower()
    matched_keywords = [kw for kw in CONTROL_KEYWORDS if kw in query_lower]

    # Step 2: spaCy sentence count
    doc = nlp(query)
    sentence_count = len(list(doc.sents))

    # Step 3: TF-IDF matching
    top_matches = tfidf_match(query, nist_controls, body.top_n)

    return {
        "input": query,
        "processing_steps": {
            "step_1_keyword_detection": {
                "description": "Scanned text for regulatory compliance keywords",
                "matched_keywords": matched_keywords,
                "keyword_count": len(matched_keywords)
            },
            "step_2_nlp_processing": {
                "description": "spaCy sentence segmentation",
                "sentence_count": sentence_count,
                "is_compliance_clause": len(matched_keywords) > 0
            },
            "step_3_tfidf_matching": {
                "description": "TF-IDF cosine similarity against 106 NIST CSF 2.0 controls",
                "method": "TF-IDF vectorization with unigram+bigram features",
                "corpus_size": len(nist_controls)
            }
        },
        "top_nist_matches": top_matches,
        "best_match": top_matches[0] if top_matches else None
    }

@router.get("/iso/{control_id}")
def search_iso_control(control_id: str):
    """
    Input: ISO control ID (e.g. A.5.1)
    Output: the control text + live NIST mapping
    """
    iso_data = load_iso()
    key = f"ISO_27001_{control_id}"

    if key in iso_data:
        m = iso_data[key]
        return {
            "source_control": {
                "id": m["source_control_id"],
                "title": m["source_control_title"],
                "text": m["source_control_text"],
                "category": m.get("source_category", "N/A")
            },
            "pre_mapped_result": {
                "nist_control_id": m["target_control_id"],
                "nist_control_title": m["target_control_title"],
                "nist_function": m.get("target_function", "N/A"),
                "confidence_score": m["confidence_score"],
                "confidence_percent": f"{round(m['confidence_score'] * 100, 1)}%",
                "gap_description": m["gap_description"] or "Full Match"
            },
            "live_tfidf_verification": live_map(
                SearchInput(query=m["source_control_text"], top_n=3)
            )["top_nist_matches"]
        }
    else:
        # Live mapping even if not in pre-loaded dataset
        nist_controls = load_nist()
        top = tfidf_match(control_id, nist_controls, 3)
        return {
            "source_control": {"id": control_id, "text": control_id},
            "note": "Not in pre-loaded dataset — live TF-IDF match only",
            "live_tfidf_result": top
        }

@router.get("/analytics")
def get_analytics():
    """
    Full analytics for dashboard — controls, confidence, coverage
    """
    iso_data = load_iso()
    values = list(iso_data.values())

    confidences = [m["confidence_score"] for m in values]
    full = [m for m in values if m["gap_description"] is None]
    partial = [m for m in values if m["gap_description"] is not None]

    categories = {}
    functions = {}
    confidence_dist = {"90-100%": 0, "80-89%": 0, "70-79%": 0, "Below 70%": 0}

    for m in values:
        cat = m.get("source_category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1
        fn = m.get("target_function", "Unknown")
        functions[fn] = functions.get(fn, 0) + 1
        c = m["confidence_score"]
        if c >= 0.90: confidence_dist["90-100%"] += 1
        elif c >= 0.80: confidence_dist["80-89%"] += 1
        elif c >= 0.70: confidence_dist["70-79%"] += 1
        else: confidence_dist["Below 70%"] += 1

    return {
        "total_controls": len(values),
        "full_coverage": len(full),
        "partial_coverage": len(partial),
        "coverage_percentage": round(len(full) / len(values) * 100, 1),
        "average_confidence": round(sum(confidences) / len(confidences) * 100, 1),
        "max_confidence": round(max(confidences) * 100, 1),
        "min_confidence": round(min(confidences) * 100, 1),
        "category_breakdown": categories,
        "nist_function_breakdown": functions,
        "confidence_distribution": confidence_dist
    }
