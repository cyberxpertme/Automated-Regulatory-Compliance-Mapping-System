# upload.py
# Phase 12: File upload with auto NLP mapping (with better error handling)

from fastapi import APIRouter, UploadFile, File, HTTPException
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pdfplumber
import spacy
import json
import os
import io

router = APIRouter(prefix="/upload", tags=["File Upload & Auto Mapping"])

nlp = spacy.load("en_core_web_sm")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NIST_FILE = os.path.join(BASE_DIR, "mappings", "nist_csf_controls.json")

CONTROL_KEYWORDS = [
    "shall", "must", "should", "required", "mandatory",
    "ensure", "establish", "maintain", "implement", "document",
    "review", "monitor", "assess", "control", "protect",
    "define", "develop", "manage", "apply", "perform"
]

def load_nist_controls():
    with open(NIST_FILE, "r") as f:
        data = json.load(f)
    return data["controls"]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF with robust error handling"""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception:
                    continue  # Skip pages that fail to extract
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Could not read PDF file. It may be corrupted, password-protected, "
                   f"or a scanned image without text. Try a different PDF or use a TXT file. "
                   f"(Error: {str(e)[:100]})"
        )
    return text

def extract_clauses(text: str):
    doc = nlp(text)
    clauses = []
    for i, sent in enumerate(doc.sents):
        sentence = sent.text.strip()
        if len(sentence.split()) < 5:
            continue
        sentence_lower = sentence.lower()
        matched = [kw for kw in CONTROL_KEYWORDS if kw in sentence_lower]
        if matched:
            clauses.append({
                "clause_id": f"UPLOADED_CLAUSE_{i+1}",
                "text": sentence,
                "matched_keywords": matched
            })
    return clauses

def match_clause_to_nist(clause_text: str, nist_controls: list):
    nist_texts = [c["title"] for c in nist_controls]
    all_texts = [clause_text] + nist_texts
    vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(all_texts)
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
    best_idx = similarities.argmax()
    best_score = float(similarities[best_idx])
    confidence = round(min(0.5 + (best_score * 0.49), 0.99), 2)
    return {
        "control_id": nist_controls[best_idx]["id"],
        "control_title": nist_controls[best_idx]["title"],
        "function": nist_controls[best_idx]["function"],
        "confidence": confidence
    }

@router.post("/analyze")
async def analyze_uploaded_file(file: UploadFile = File(...)):
    """Upload a PDF or text file and auto-map clauses to NIST CSF"""

    if not file.filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported")

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")

    # Extract text
    if file.filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    else:
        try:
            text = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Could not decode text file. Make sure it's UTF-8 encoded.")

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="No readable text found in this file. If it's a scanned PDF (image-based), "
                   "text extraction won't work — please try a text-based PDF or a TXT file."
        )

    clauses = extract_clauses(text)

    if not clauses:
        return {
            "filename": file.filename,
            "total_clauses_found": 0,
            "message": "No compliance clauses detected. Try a document with regulatory language (shall, must, ensure, etc).",
            "mappings": []
        }

    nist_controls = load_nist_controls()
    results = []
    for clause in clauses[:30]:
        match = match_clause_to_nist(clause["text"], nist_controls)
        results.append({
            "source_text": clause["text"],
            "source_keywords": clause["matched_keywords"],
            "matched_nist_control": match["control_id"],
            "matched_nist_title": match["control_title"],
            "nist_function": match["function"],
            "confidence_score": match["confidence"]
        })

    avg_confidence = round(sum(r["confidence_score"] for r in results) / len(results) * 100, 1)

    return {
        "filename": file.filename,
        "total_clauses_found": len(clauses),
        "total_mapped": len(results),
        "average_confidence": avg_confidence,
        "mappings": results
    }
