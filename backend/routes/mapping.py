# mapping.py
# Phase 5: Compliance mapping API
# Maps ISO 27001 controls to NIST CSF with confidence scoring

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from models.compliance import ControlMapping
from routes.auth import get_current_user
from models.user import User
import json
import os

router = APIRouter(prefix="/mapping", tags=["Compliance Mapping"])

# Load mapping data from JSON file
MAPPING_FILE = os.path.join(
    os.path.dirname(__file__),
    "../mappings/iso_nist_sample.json"
)

def load_mappings():
    with open(MAPPING_FILE, "r") as f:
        return json.load(f)

# --- Routes ---

@router.get("/sample")
def get_sample_mappings():
    """
    Get all ISO 27001 to NIST CSF mappings.
    No auth required — for demo and testing.
    """
    mappings = load_mappings()
    return {
        "total": len(mappings),
        "source_framework": "ISO_27001",
        "target_framework": "NIST_CSF",
        "mappings": list(mappings.values())
    }

@router.get("/stats")
def get_stats():
    """
    Get compliance statistics for dashboard.
    Shows coverage percentage and average confidence.
    """
    mappings = load_mappings()
    values = list(mappings.values())

    full = [m for m in values if m["gap_description"] is None]
    partial = [m for m in values if m["gap_description"] is not None]
    avg_conf = sum(m["confidence_score"] for m in values) / len(values)

    return {
        "total_controls": len(values),
        "full_coverage": len(full),
        "partial_coverage": len(partial),
        "coverage_percentage": round((len(full) / len(values)) * 100, 1),
        "average_confidence": round(avg_conf * 100, 1),
        "frameworks": {
            "source": "ISO 27001:2022",
            "target": "NIST CSF 2.0"
        }
    }

@router.get("/search/{control_id}")
def search_mapping(control_id: str):
    """
    Search for a specific ISO 27001 control mapping.
    Example: /mapping/search/A.5.1
    """
    mappings = load_mappings()
    key = f"ISO_27001_{control_id}"
    if key not in mappings:
        raise HTTPException(
            status_code=404,
            detail=f"Control {control_id} not found"
        )
    return mappings[key]

@router.post("/seed-db")
def seed_database(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Seed database with sample mappings.
    Requires authentication.
    """
    mappings = load_mappings()
    count = 0

    for key, m in mappings.items():
        existing = db.query(ControlMapping).filter(
            ControlMapping.source_control_id == m["source_control_id"]
        ).first()

        if not existing:
            record = ControlMapping(
                source_framework=m["source_framework"],
                source_control_id=m["source_control_id"],
                source_control_title=m["source_control_title"],
                source_control_text=m["source_control_text"],
                target_framework=m["target_framework"],
                target_control_id=m["target_control_id"],
                target_control_title=m["target_control_title"],
                confidence_score=m["confidence_score"],
                gap_description=m["gap_description"],
            )
            db.add(record)
            count += 1

    db.commit()
    return {
        "message": f"Successfully seeded {count} mappings",
        "total_in_db": db.query(ControlMapping).count()
    }

@router.get("/from-db")
def get_from_db(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all mappings from database.
    Requires authentication.
    """
    mappings = db.query(ControlMapping).all()
    return {
        "total": len(mappings),
        "mappings": mappings
    }
