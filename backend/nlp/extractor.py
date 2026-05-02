import spacy
from typing import List, Dict

nlp = spacy.load("en_core_web_sm")

CONTROL_KEYWORDS = [
    "shall", "must", "should", "required", "mandatory",
    "ensure", "establish", "maintain", "implement", "document",
    "review", "monitor", "assess", "control", "protect"
]

def extract_clauses(text: str, framework: str = "UNKNOWN") -> List[Dict]:
    doc = nlp(text)
    clauses = []
    for i, sent in enumerate(doc.sents):
        sentence = sent.text.strip()
        if len(sentence.split()) < 5:
            continue
        sentence_lower = sentence.lower()
        matched = [kw for kw in CONTROL_KEYWORDS if kw in sentence_lower]
        if matched:
            confidence = min(0.5 + (len(matched) * 0.1), 0.99)
            clauses.append({
                "clause_id": f"{framework}_CLAUSE_{i+1}",
                "text": sentence,
                "framework": framework,
                "matched_keywords": matched,
                "confidence": round(confidence, 2),
                "type": "control"
            })
    return clauses
