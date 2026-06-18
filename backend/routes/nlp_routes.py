# nlp_routes.py
# Phase 9: Updated NLP endpoints with TF-IDF scoring

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from nlp.extractor import extract_clauses

router = APIRouter(prefix="/nlp", tags=["NLP Engine"])

# Real ISO 27001 sample text
SAMPLE_ISO_TEXT = """
5.1 Policies for information security
A set of policies for information security shall be defined, approved by
management, published and communicated to employees and relevant external
parties. The policies shall be reviewed at planned intervals or when
significant changes occur to ensure their continuing suitability.

5.2 Information security roles and responsibilities
All information security responsibilities shall be defined and allocated
to specific roles within the organization. Responsibilities shall be
documented and communicated to relevant personnel.

6.1 Actions to address risks and opportunities
The organization shall plan actions to address these risks and
opportunities. The organization shall implement the actions into its
information security management system processes and evaluate the
effectiveness of these actions.

8.2 Information security risk assessment
The organization shall perform information security risk assessments
at planned intervals or when significant changes are proposed or occur.
Risk assessments shall produce consistent, valid and comparable results.
The organization shall retain documented information about the results.

9.1 Monitoring, measurement, analysis and evaluation
The organization shall evaluate the information security performance
and the effectiveness of the information security management system.
The organization shall determine what needs to be monitored and measured.
The organization shall retain documented information as evidence.

10.1 Continual improvement
The organization shall continually improve the suitability, adequacy
and effectiveness of the information security management system.
"""

class TextInput(BaseModel):
    text: str
    framework: str = "UNKNOWN"

@router.post("/extract")
def extract_from_text(body: TextInput):
    """Extract compliance clauses with TF-IDF confidence scoring"""
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    clauses = extract_clauses(body.text, body.framework)
    avg_confidence = round(
        sum(c["confidence"] for c in clauses) / len(clauses) * 100, 1
    ) if clauses else 0
    return {
        "total_clauses_found": len(clauses),
        "average_confidence": avg_confidence,
        "framework": body.framework,
        "scoring_method": "TF-IDF + Keyword Boost",
        "clauses": clauses
    }

@router.get("/demo")
def run_demo():
    """Run TF-IDF NLP demo on real ISO 27001 sample text"""
    clauses = extract_clauses(SAMPLE_ISO_TEXT, "ISO_27001")
    avg_confidence = round(
        sum(c["confidence"] for c in clauses) / len(clauses) * 100, 1
    ) if clauses else 0
    return {
        "message": "Phase 9: TF-IDF NLP extraction from ISO 27001",
        "total_clauses_found": len(clauses),
        "average_confidence": avg_confidence,
        "scoring_method": "TF-IDF + Keyword Boost",
        "clauses": clauses
    }
