# upload.py
# Phase 13+14: Multi-file upload, NLP+TF-IDF mapping, DB persistence, PDF export

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime
from models.database import get_db
from models.upload_history import UploadHistory, UploadClause
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
        return json.load(f)["controls"]

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception:
                    continue
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {str(e)[:100]}")
    return text

def extract_clauses(text: str, source_file: str):
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
                "clause_id": f"{source_file}_CLAUSE_{i+1}",
                "text": sentence,
                "matched_keywords": matched,
                "source_file": source_file
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

def process_single_file(filename: str, file_bytes: bytes):
    if not filename.lower().endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail=f"{filename}: only PDF/TXT supported")
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail=f"{filename}: file is empty")

    if filename.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_bytes)
    else:
        try:
            text = file_bytes.decode('utf-8')
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail=f"{filename}: could not decode as UTF-8 text")

    if not text.strip():
        raise HTTPException(status_code=400, detail=f"{filename}: no readable text found")

    clauses = extract_clauses(text, filename)
    nist_controls = load_nist_controls()

    results = []
    for clause in clauses[:30]:
        match = match_clause_to_nist(clause["text"], nist_controls)
        results.append({
            "source_file": filename,
            "source_text": clause["text"],
            "source_keywords": clause["matched_keywords"],
            "matched_nist_control": match["control_id"],
            "matched_nist_title": match["control_title"],
            "nist_function": match["function"],
            "confidence_score": match["confidence"]
        })
    return results

@router.post("/analyze-multi")
async def analyze_multiple_files(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload 2+ files. Extract+map clauses with NLP+TF-IDF,
    SAVE the result permanently to PostgreSQL, return combined stats.
    """
    if len(files) == 0:
        raise HTTPException(status_code=400, detail="No files uploaded")

    all_mappings = []
    file_summaries = []
    errors = []

    for f in files:
        try:
            file_bytes = await f.read()
            results = process_single_file(f.filename, file_bytes)
            all_mappings.extend(results)
            file_summaries.append({
                "filename": f.filename,
                "clauses_found": len(results),
                "average_confidence": round(
                    sum(r["confidence_score"] for r in results) / len(results) * 100, 1
                ) if results else 0
            })
        except HTTPException as e:
            errors.append({"filename": f.filename, "error": e.detail})

    if not all_mappings:
        raise HTTPException(status_code=400, detail=f"No clauses extracted. Errors: {errors}")

    avg_confidence = round(sum(m["confidence_score"] for m in all_mappings) / len(all_mappings) * 100, 1)
    function_counts = {}
    for m in all_mappings:
        fn = m["nist_function"]
        function_counts[fn] = function_counts.get(fn, 0) + 1
    high_conf = len([m for m in all_mappings if m["confidence_score"] >= 0.85])
    low_conf = len(all_mappings) - high_conf

    # --- SAVE TO DATABASE (Phase 14) ---
    history_record = UploadHistory(
        uploaded_by="anonymous",  # could be replaced with current_user.email if auth required
        total_files=len(files),
        total_clauses_mapped=len(all_mappings),
        average_confidence=avg_confidence,
        high_confidence_count=high_conf,
        low_confidence_count=low_conf,
        file_breakdown=json.dumps(file_summaries),
        function_distribution=json.dumps(function_counts)
    )
    db.add(history_record)
    db.commit()
    db.refresh(history_record)

    for m in all_mappings:
        db.add(UploadClause(
            upload_id=history_record.id,
            source_file=m["source_file"],
            source_text=m["source_text"],
            matched_nist_control=m["matched_nist_control"],
            matched_nist_title=m["matched_nist_title"],
            nist_function=m["nist_function"],
            confidence_score=m["confidence_score"]
        ))
    db.commit()

    combined_stats = {
        "upload_id": history_record.id,
        "total_files": len(files),
        "successful_files": len(file_summaries),
        "failed_files": len(errors),
        "total_clauses_mapped": len(all_mappings),
        "average_confidence": avg_confidence,
        "high_confidence_count": high_conf,
        "low_confidence_count": low_conf,
        "function_distribution": function_counts,
        "file_breakdown": file_summaries,
        "errors": errors,
        "generated_at": datetime.now().isoformat()
    }

    return {
        "message": f"Processed {len(file_summaries)} of {len(files)} files and saved to database",
        "combined_stats": combined_stats,
        "mappings": all_mappings
    }

@router.get("/live-stats")
def get_live_upload_stats(db: Session = Depends(get_db)):
    """Get the MOST RECENT upload batch from the database (persists across restarts)"""
    latest = db.query(UploadHistory).order_by(UploadHistory.id.desc()).first()
    if not latest:
        return {"has_data": False, "message": "No documents uploaded yet"}

    return {
        "has_data": True,
        "upload_id": latest.id,
        "total_files": latest.total_files,
        "total_clauses_mapped": latest.total_clauses_mapped,
        "average_confidence": latest.average_confidence,
        "high_confidence_count": latest.high_confidence_count,
        "low_confidence_count": latest.low_confidence_count,
        "function_distribution": json.loads(latest.function_distribution or "{}"),
        "file_breakdown": json.loads(latest.file_breakdown or "[]"),
        "created_at": latest.created_at.isoformat() if latest.created_at else None
    }

@router.get("/history")
def get_upload_history(db: Session = Depends(get_db)):
    """List all past upload batches — shows project growth over time"""
    records = db.query(UploadHistory).order_by(UploadHistory.id.desc()).all()
    return {
        "total_batches": len(records),
        "history": [
            {
                "upload_id": r.id,
                "total_files": r.total_files,
                "total_clauses_mapped": r.total_clauses_mapped,
                "average_confidence": r.average_confidence,
                "created_at": r.created_at.isoformat() if r.created_at else None
            }
            for r in records
        ]
    }

@router.get("/download-report")
def download_upload_report(db: Session = Depends(get_db)):
    """Generate PDF report from the MOST RECENT upload batch in the database"""
    latest = db.query(UploadHistory).order_by(UploadHistory.id.desc()).first()
    if not latest:
        raise HTTPException(status_code=404, detail="No uploaded document analysis available yet")

    clauses = db.query(UploadClause).filter(UploadClause.upload_id == latest.id).all()
    file_breakdown = json.loads(latest.file_breakdown or "[]")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)

    DARK_BLUE = HexColor('#0A0F2E')
    CYAN = HexColor('#00D4FF')
    LIGHT_GRAY = HexColor('#F1F5F9')
    DARK_GRAY = HexColor('#334155')

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=18, textColor=DARK_BLUE,
        spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('S', parent=styles['Normal'], fontSize=10, textColor=DARK_GRAY,
        spaceAfter=4, alignment=TA_CENTER)
    heading_style = ParagraphStyle('H', parent=styles['Heading2'], fontSize=12, textColor=DARK_BLUE,
        spaceBefore=14, spaceAfter=6, fontName='Helvetica-Bold')
    normal_style = ParagraphStyle('N', parent=styles['Normal'], fontSize=8, textColor=DARK_GRAY)

    story = []
    story.append(Paragraph("🛡️ Uploaded Document Compliance Analysis Report", title_style))
    story.append(Paragraph("Automatic NLP + TF-IDF Mapping to NIST CSF 2.0 (Saved in Database)", subtitle_style))
    story.append(Paragraph("University of Dhaka | PMICS Batch 4 | H-411 & H-392", subtitle_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=CYAN, spaceAfter=14))

    story.append(Paragraph("Executive Summary", heading_style))
    summary_data = [
        ["Metric", "Value"],
        ["Files Uploaded", str(latest.total_files)],
        ["Total Clauses Mapped", str(latest.total_clauses_mapped)],
        ["Average Confidence", f"{latest.average_confidence}%"],
        ["High Confidence (>=85%)", str(latest.high_confidence_count)],
        ["Low Confidence (<85%)", str(latest.low_confidence_count)],
        ["Upload Date", latest.created_at.strftime("%Y-%m-%d %H:%M") if latest.created_at else "N/A"],
    ]
    t = Table(summary_data, colWidths=[3*inch, 3*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE), ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.5, DARK_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Files Processed", heading_style))
    file_data = [["Filename", "Clauses Found", "Avg Confidence"]]
    for f in file_breakdown:
        file_data.append([f["filename"], str(f["clauses_found"]), f"{f['average_confidence']}%"])
    ft = Table(file_data, colWidths=[3.5*inch, 1.5*inch, 1.5*inch])
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1E3A5F')), ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.5, DARK_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(ft)
    story.append(Spacer(1, 12))

    story.append(Paragraph("Extracted Clause to NIST CSF Mapping", heading_style))
    map_data = [["File", "Extracted Clause", "NIST Control", "Confidence"]]
    for c in clauses[:60]:
        map_data.append([
            c.source_file,
            Paragraph(c.source_text[:90], normal_style),
            c.matched_nist_control,
            f"{round(c.confidence_score*100)}%"
        ])
    mt = Table(map_data, colWidths=[1.2*inch, 3.3*inch, 1*inch, 1*inch])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE), ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTSIZE', (0,1), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.3, DARK_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(mt)

    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=1, color=CYAN, spaceAfter=6))
    story.append(Paragraph(
        "Generated by Automated Regulatory Compliance Mapping System | "
        "University of Dhaka — PMICS Batch 4 | H-411 & H-392", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    filename = f"uploaded_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(buffer, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"})
