# extractor.py
# Phase 9: Improved NLP with TF-IDF similarity scoring

import spacy
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Control keywords for clause detection
CONTROL_KEYWORDS = [
    "shall", "must", "should", "required", "mandatory",
    "ensure", "establish", "maintain", "implement", "document",
    "review", "monitor", "assess", "control", "protect",
    "define", "develop", "manage", "apply", "perform",
    "verify", "validate", "authorize", "restrict", "prevent"
]

# NIST CSF reference controls for TF-IDF matching
NIST_REFERENCE = [
    "organizational cybersecurity policy is established and communicated",
    "roles and responsibilities for cybersecurity risk management are established",
    "identities and credentials for authorized users are managed",
    "access permissions and authorizations are managed reviewed and modified",
    "users services and hardware are authenticated",
    "personnel are provided with awareness and training",
    "backups of data are created protected maintained and tested",
    "log records are generated to enable monitoring and incident response",
    "networks and network services are monitored for anomalous behavior",
    "vulnerabilities in assets are identified validated and recorded",
    "cyber threat intelligence is received from information sharing forums",
    "configuration management practices are established and documented",
    "secure software development practices are integrated into development",
    "physical access to assets is managed monitored and enforced",
    "the physical environment is monitored for potential threats",
    "cybersecurity supply chain risk management policy is established",
    "incidents are contained eradicated and recovery actions performed",
    "backups of data are created protected maintained and tested regularly",
    "information security risks are identified assessed and treated",
    "cryptographic controls are used to protect data confidentiality"
]

def calculate_tfidf_confidence(text: str, reference_texts: List[str]) -> float:
    """
    Calculate confidence using TF-IDF cosine similarity.
    Higher similarity = higher confidence score.
    """
    try:
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=500
        )
        all_texts = [text] + reference_texts
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        
        # Compare input text with all reference texts
        similarities = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:]
        )[0]
        
        # Take the highest similarity score
        max_similarity = float(np.max(similarities))
        
        # Scale to 0.5 - 0.99 range
        confidence = 0.5 + (max_similarity * 0.49)
        return round(min(confidence, 0.99), 2)
    except:
        return 0.60

def extract_clauses(text: str, framework: str = "UNKNOWN") -> List[Dict]:
    """
    Extract compliance clauses using spaCy + TF-IDF scoring.
    Phase 9: More accurate confidence with semantic similarity.
    """
    doc = nlp(text)
    clauses = []

    for i, sent in enumerate(doc.sents):
        sentence = sent.text.strip()

        # Skip very short sentences
        if len(sentence.split()) < 5:
            continue

        sentence_lower = sentence.lower()

        # Find matched keywords
        matched = [kw for kw in CONTROL_KEYWORDS if kw in sentence_lower]

        if matched:
            # Phase 9: TF-IDF based confidence
            tfidf_conf = calculate_tfidf_confidence(
                sentence_lower,
                NIST_REFERENCE
            )

            # Keyword boost
            keyword_boost = min(len(matched) * 0.02, 0.10)
            confidence = min(tfidf_conf + keyword_boost, 0.99)

            clauses.append({
                "clause_id": f"{framework}_CLAUSE_{i+1}",
                "text": sentence,
                "framework": framework,
                "matched_keywords": matched,
                "confidence": round(confidence, 2),
                "scoring_method": "TF-IDF + Keyword Boost",
                "type": "control"
            })

    return clauses
