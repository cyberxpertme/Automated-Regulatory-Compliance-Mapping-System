# reports.py
# Phase 10+11: PDF report generation supporting all frameworks

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime
import json
import os

router = APIRouter(prefix="/reports", tags=["Reports"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FRAMEWORK_FILES = {
    "iso27001": "complete_iso_nist_mapping.json",
    "pci_dss": "pci_dss_nist_mapping.json"
}

def load_all_mappings():
    """Load and combine mappings from ALL frameworks"""
    all_values = []
    for fw_id, filename in FRAMEWORK_FILES.items():
        filepath = os.path.join(BASE_DIR, "mappings", filename)
        with open(filepath, "r") as f:
            data = json.load(f)
            all_values.extend(list(data.values()))
    return all_values

def generate_pdf_report():
    """Generate compliance report PDF covering ALL frameworks"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=0.75*inch, leftMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch
    )

    DARK_BLUE = HexColor('#0A0F2E')
    CYAN = HexColor('#00D4FF')
    LIGHT_GRAY = HexColor('#F1F5F9')
    DARK_GRAY = HexColor('#334155')

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'], fontSize=20,
        textColor=DARK_BLUE, spaceAfter=8, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=11,
        textColor=DARK_GRAY, spaceAfter=4, alignment=TA_CENTER)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=13,
        textColor=DARK_BLUE, spaceBefore=16, spaceAfter=8, fontName='Helvetica-Bold')
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=9,
        textColor=DARK_GRAY, spaceAfter=4)

    story = []
    story.append(Paragraph("🛡️ Automated Regulatory Compliance Mapping System", title_style))
    story.append(Paragraph("Multi-Framework Compliance Report (ISO 27001 + PCI-DSS → NIST CSF)", subtitle_style))
    story.append(Paragraph("University of Dhaka | PMICS Batch 4 | H-411 & H-392", subtitle_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=CYAN, spaceAfter=16))

    values = load_all_mappings()
    full = [m for m in values if m["gap_description"] is None]
    partial = [m for m in values if m["gap_description"] is not None]
    avg_conf = sum(m["confidence_score"] for m in values) / len(values)

    # Framework breakdown
    fw_counts = {}
    for m in values:
        fw = m.get("source_framework", "Unknown")
        fw_counts[fw] = fw_counts.get(fw, 0) + 1

    story.append(Paragraph("Executive Summary", heading_style))
    summary_data = [["Metric", "Value"]]
    summary_data.append(["Total Controls Mapped (All Frameworks)", str(len(values))])
    for fw, count in fw_counts.items():
        summary_data.append([f"  - {fw} Controls", str(count)])
    summary_data.append(["Full Coverage Mappings", f"{len(full)} ({round(len(full)/len(values)*100, 1)}%)"])
    summary_data.append(["Partial Coverage Mappings", f"{len(partial)} ({round(len(partial)/len(values)*100, 1)}%)"])
    summary_data.append(["Average Confidence Score", f"{round(avg_conf * 100, 1)}%"])
    summary_data.append(["Target Framework", "NIST CSF 2.0"])
    summary_data.append(["Report Date", datetime.now().strftime("%Y-%m-%d")])

    summary_table = Table(summary_data, colWidths=[3.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # Complete mapping table for ALL frameworks
    story.append(Paragraph("Complete Control Mapping Details (All Frameworks)", heading_style))
    table_data = [["Framework", "Control ID", "Title", "NIST CSF", "Confidence", "Status"]]
    for m in values:
        conf_pct = f"{round(m['confidence_score'] * 100)}%"
        status = "Full Match" if m["gap_description"] is None else "Partial"
        table_data.append([
            m["source_framework"],
            m["source_control_id"],
            Paragraph(m["source_control_title"][:35], normal_style),
            m["target_control_id"],
            conf_pct,
            status
        ])

    mapping_table = Table(table_data, colWidths=[0.8*inch, 0.7*inch, 2.3*inch, 0.9*inch, 0.8*inch, 0.8*inch])
    mapping_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.3, DARK_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(mapping_table)
    story.append(Spacer(1, 16))

    if partial:
        story.append(Paragraph("Gap Analysis", heading_style))
        gap_data = [["Framework", "Control", "Gap Description"]]
        for m in partial:
            gap_data.append([
                m["source_framework"],
                m["source_control_id"],
                Paragraph(m["gap_description"] or "", normal_style)
            ])
        gap_table = Table(gap_data, colWidths=[1.2*inch, 1.0*inch, 4.8*inch])
        gap_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#7C3AED')),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#FEF3C7')]),
            ('GRID', (0, 0), (-1, -1), 0.3, DARK_GRAY),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(gap_table)

    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="100%", thickness=1, color=CYAN, spaceAfter=8))
    story.append(Paragraph(
        "Generated by Automated Regulatory Compliance Mapping System | "
        "University of Dhaka — PMICS Batch 4 | H-411 & H-392", subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

@router.get("/download")
def download_report():
    """Download multi-framework compliance report as PDF"""
    pdf_buffer = generate_pdf_report()
    filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(
        pdf_buffer, media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/preview")
def preview_report():
    values = load_all_mappings()
    full = [m for m in values if m["gap_description"] is None]
    partial = [m for m in values if m["gap_description"] is not None]
    avg_conf = sum(m["confidence_score"] for m in values) / len(values)
    return {
        "report_title": "Multi-Framework Compliance Report",
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_controls": len(values),
            "full_coverage": len(full),
            "partial_coverage": len(partial),
            "average_confidence": round(avg_conf * 100, 1)
        }
    }
