from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter(prefix="/frameworks", tags=["Multi-Framework"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRAMEWORK_FILES = {
    "iso27001": "complete_iso_nist_mapping.json",
    "pci_dss": "pci_dss_nist_mapping.json"
}

def load_framework(name: str):
    if name not in FRAMEWORK_FILES:
        raise HTTPException(status_code=404, detail=f"Framework '{name}' not supported")
    filepath = os.path.join(BASE_DIR, "mappings", FRAMEWORK_FILES[name])
    with open(filepath, "r") as f:
        return json.load(f)

@router.get("/list")
def list_frameworks():
    return {
        "supported_frameworks": [
            {"id": "iso27001", "name": "ISO 27001:2022", "description": "Information Security Management System standard"},
            {"id": "pci_dss", "name": "PCI-DSS v4.0", "description": "Payment Card Industry Data Security Standard"}
        ],
        "target_framework": "NIST CSF 2.0"
    }

@router.get("/{framework_id}/mappings")
def get_framework_mappings(framework_id: str):
    data = load_framework(framework_id)
    return {"framework": framework_id, "total": len(data), "mappings": list(data.values())}

@router.get("/{framework_id}/stats")
def get_framework_stats(framework_id: str):
    data = load_framework(framework_id)
    values = list(data.values())
    full = [m for m in values if m["gap_description"] is None]
    partial = [m for m in values if m["gap_description"] is not None]
    avg_conf = sum(m["confidence_score"] for m in values) / len(values)
    categories = {}
    for m in values:
        cat = m.get("source_category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1
    return {
        "framework": framework_id,
        "total_controls": len(values),
        "full_coverage": len(full),
        "partial_coverage": len(partial),
        "coverage_percentage": round((len(full) / len(values)) * 100, 1),
        "average_confidence": round(avg_conf * 100, 1),
        "categories": categories
    }

@router.get("/combined/stats")
def get_combined_stats():
    all_values = []
    breakdown = {}
    for fw_id in FRAMEWORK_FILES.keys():
        data = load_framework(fw_id)
        values = list(data.values())
        all_values.extend(values)
        breakdown[fw_id] = len(values)
    full = [m for m in all_values if m["gap_description"] is None]
    partial = [m for m in all_values if m["gap_description"] is not None]
    avg_conf = sum(m["confidence_score"] for m in all_values) / len(all_values)
    return {
        "total_frameworks": len(FRAMEWORK_FILES),
        "total_controls_all_frameworks": len(all_values),
        "framework_breakdown": breakdown,
        "full_coverage": len(full),
        "partial_coverage": len(partial),
        "overall_average_confidence": round(avg_conf * 100, 1)
    }
