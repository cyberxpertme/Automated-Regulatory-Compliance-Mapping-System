# reports.py
# Phase 10: PDF compliance report generation

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from io import BytesIO
from datetime import datetime
import json
import os

router = APIRouter(prefix="/reports", tags=["Reports"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAPPING_FILE = os.path.join(BASE_DIR, "mappings", "complete_iso_nist_mapping.json")

def load_mappings():
    with open(MAPPING_FILE, "r") as f:
        return json.load(f)

def generate_pdf_report():
    """Generate professional compliance report PDF"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Colors
    DARK_BLUE = HexColor('#0A0F2E')
    CYAN = HexColor('#00D4FF')
    GREEN = HexColor('#22C55E')
    ORANGE = HexColor('#F59E0B')
    LIGHT_GRAY = HexColor('#F1F5F9')
    DARK_GRAY = HexColor('#334155')

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=20,
        textColor=DARK_BLUE,
        spaceAfter=8,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=DARK_GRAY,
        spaceAfter=4,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=DARK_BLUE,
        spaceBefore=16,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        textColor=DARK_GRAY,
        spaceAfter=4
    )

    story = []

    # Header
    story.append(Paragraph(
        "🛡️ Automated Regulatory Compliance Mapping System",
        title_style
    ))
    story.append(Paragraph(
        "ISO 27001:2022 → NIST CSF 2.0 Compliance Report",
        subtitle_style
    ))
    story.append(Paragraph(
        "University of Dhaka | PMICS Batch 4 | H-411 & H-392",
        subtitle_style
    ))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        subtitle_style
    ))
    story.append(HRFlowable(
        width="100%", thickness=2,
        color=CYAN, spaceAfter=16
    ))

    # Load data
    mappings = load_mappings()
    values = list(mappings.values())
    full = [m for m in values if m["gap_description"] is None]
    partial = [m for m in values if m["gap_description"] is not None]
    avg_conf = sum(m["confidence_score"] for m in values) / len(values)

    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))

    summary_data = [
        ["Metric", "Value"],
        ["Total ISO 27001 Controls Mapped", str(len(values))],
        ["Full Coverage Mappings", f"{len(full)} ({round(len(full)/len(values)*100, 1)}%)"],
        ["Partial Coverage Mappings", f"{len(partial)} ({round(len(partial)/len(values)*100, 1)}%)"],
        ["Average Confidence Score", f"{round(avg_conf * 100, 1)}%"],
        ["Source Framework", "ISO 27001:2022"],
        ["Target Framework", "NIST CSF 2.0"],
        ["Report Date", datetime.now().strftime("%Y-%m-%d")],
    ]

    summary_table = Table(summary_data, colWidths=[3.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
        ('ROUNDEDCORNERS', [3]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # Category Breakdown
    story.append(Paragraph("Control Categories", heading_style))
    categories = {}
    for m in values:
        cat = m.get("source_category", "Unknown")
        categories[cat] = categories.get(cat, 0) + 1

    cat_data = [["Category", "Count", "Percentage"]]
    for cat, count in categories.items():
        cat_data.append([
            cat,
            str(count),
            f"{round(count/len(values)*100, 1)}%"
        ])

    cat_table = Table(cat_data, colWidths=[3.5*inch, 1.5*inch, 2*inch])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1E3A5F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.5, DARK_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 16))

    # Complete Mapping Table
    story.append(Paragraph("Complete Control Mapping Details", heading_style))

    table_data = [[
        "ISO 27001", "Title", "NIST CSF",
        "Confidence", "Status"
    ]]

    for m in values:
        conf_pct = f"{round(m['confidence_score'] * 100)}%"
        status = "Full Match" if m["gap_description"] is None else "Partial"
        table_data.append([
            m["source_control_id"],
            Paragraph(m["source_control_title"][:40], normal_style),
            m["target_control_id"],
            conf_pct,
            status
        ])

    mapping_table = Table(
        table_data,
        colWidths=[0.8*inch, 2.8*inch, 1.0*inch, 0.9*inch, 1.5*inch]
    )
    mapping_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LIGHT_GRAY]),
        ('GRID', (0, 0), (-1, -1), 0.3, DARK_GRAY),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(mapping_table)
    story.append(Spacer(1, 16))

    # Gap Analysis
    if partial:
        story.append(Paragraph("Gap Analysis", heading_style))
        gap_data = [["Control", "Title", "Gap Description"]]
        for m in partial:
            gap_data.append([
                m["source_control_id"],
                Paragraph(m["source_control_title"], normal_style),
                Paragraph(m["gap_description"] or "", normal_style)
            ])
        gap_table = Table(
            gap_data,
            colWidths=[0.8*inch, 2.0*inch, 4.2*inch]
        )
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

    # Footer
    story.append(Spacer(1, 24))
    story.append(HRFlowable(
        width="100%", thickness=1,
        color=CYAN, spaceAfter=8
    ))
    story.append(Paragraph(
        "Generated by Automated Regulatory Compliance Mapping System | "
        "University of Dhaka — PMICS Batch 4 | H-411 & H-392",
        subtitle_style
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer

@router.get("/download")
def download_report():
    """Download compliance report as PDF"""
    pdf_buffer = generate_pdf_report()
    filename = f"compliance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )

@router.get("/preview")
def preview_report():
    """Preview report stats before downloading"""
    mappings = load_mappings()
    values = list(mappings.values())
    full = [m for m in values if m["gap_description"] is None]
    partial = [m for m in values if m["gap_description"] is not None]
    avg_conf = sum(m["confidence_score"] for m in values) / len(values)
    return {
        "report_title": "ISO 27001 → NIST CSF Compliance Report",
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_controls": len(values),
            "full_coverage": len(full),
            "partial_coverage": len(partial),
            "average_confidence": round(avg_conf * 100, 1)
        }
    }
