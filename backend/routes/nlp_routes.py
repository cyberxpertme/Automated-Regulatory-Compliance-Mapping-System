from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from nlp.extractor import extract_clauses

router = APIRouter(prefix="/nlp", tags=["NLP Engine"])

SAMPLE_ISO_TEXT = """
5.1 Policies for information security
A set of policies for information security shall be defined,
approved by management, published and communicated to employees.
The policies shall be reviewed at planned intervals.

6.1 Actions to address risks and opportunities
The organization shall plan actions to address these risks.
The organization shall implement the actions into its processes.

8.2 Information security risk assessment
The organization shall perform information security risk assessments
at planned intervals or when significant changes occur.
Risk assessments shall produce consistent, valid and comparable results.

9.1 Monitoring and measurement
The organization shall evaluate the information security performance.
The organization shall retain documented information as evidence.
"""

class TextInput(BaseModel):
    text: str
    framework: str = "UNKNOWN"

@router.post("/extract")
def extract_from_text(body: TextInput):
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    clauses = extract_clauses(body.text, body.framework)
    return {
        "total_clauses_found": len(clauses),
        "framework": body.framework,
        "clauses": clauses
    }

@router.get("/demo")
def run_demo():
    clauses = extract_clauses(SAMPLE_ISO_TEXT, "ISO_27001")
    return {
        "message": "Demo extraction from ISO 27001 sample text",
        "total_clauses_found": len(clauses),
        "clauses": clauses
    }
