from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from xml.sax.saxutils import escape

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()

def generate_pdf(filename, name, age, gender, height, weight, bmi, category, water):
    """
    Generates a comprehensive PDF health report for a user's BMI and hydration tracking.
    """
    safe_name = escape(str(name))
    # Initialize the document
    doc = SimpleDocTemplate(
        filename,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        rightMargin=0.75*inch, leftMargin=0.75*inch,
        topMargin=0.75*inch, bottomMargin=0.75*inch
    )
    
    story = []
    
    # Custom Styles
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=15
    )

    today = datetime.now().strftime("%d %B %Y %I:%M %p")

    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#2D3748")
    )

    footer_style = ParagraphStyle(
    "Footer",
    parent=styles["Normal"],
    alignment=1,
    textColor=colors.grey,
    fontSize=10
)
    
    # 1. Document Header
    story.append(Paragraph("FitTrack BMI Health Report", title_style))
    subtitle_style = ParagraphStyle("Subtitle",parent=styles["Heading2"],textColor=colors.grey,alignment=1,spaceAfter=10)
    story.append(Paragraph("Your Personal Health Report",subtitle_style ))
  
    story.append(Paragraph(f"<b>Generated On:</b> {today}",body_style))

    story.append(Spacer(1,0.2*inch))
    
    # 2. Table Data (Updated with all your dynamic Streamlit variables)
    data = [
        ["Field", "Value"],
        [Paragraph("<b>Participant Name:</b>", body_style), Paragraph(safe_name, body_style)],
        [Paragraph("<b>Age / Gender:</b>", body_style), Paragraph(f"{age} years old / {gender}", body_style)],
        [Paragraph("<b>Height:</b>", body_style), Paragraph(f"{height:.2f} m", body_style)],
        [Paragraph("<b>Weight:</b>", body_style), Paragraph(f"{weight:.2f} kg", body_style)],
        [Paragraph("<b>Calculated BMI:</b>", body_style), Paragraph(f"<b>{bmi:.2f}</b>", body_style)],
        [Paragraph("<b>Classification:</b>", body_style), Paragraph(f"<b>{category}</b>", body_style)],
        [Paragraph("<b>Estimated Daily Water Intake Target:</b>", body_style), Paragraph(f"{water:.0f} ml/day", body_style)],
    ]
    
    # Clean, modern table formatting
    table = Table(data, colWidths=[2.5*inch, 4.0*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.HexColor("#E2E8F0")), # Divider lines
        ('BOX', (0,0), (-1,-1), 1, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F7FAFC")),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3 * inch))
    
    # 3. Informational Footnote Section
    story.append(Paragraph("<b>Health Information Notes:</b>", styles['Heading3']))
    story.append(Spacer(1, 0.05 * inch))
    
    info_text = (
        "Body Mass Index (BMI) is calculated from height and weight. "
        "It is a screening measure and does not directly measure body fat. "
        "Standard categories are: Underweight (<18.5), Normal (18.5–24.9), Overweight (25–29.9), "
        "and Obesity (≥30). Proper daily water consumption supports your metabolic health alongside "
        "balanced nutrition and physical activity."
    )
    story.append(Paragraph(info_text, body_style))

    story.append(Spacer(1,0.3*inch))

    story.append(Paragraph("<b>Health Tips</b>", styles["Heading3"]))
    story.append(Spacer(1, 0.1 * inch))

    if category.lower() == "normal weight":
        tips = [
            "• Maintain a balanced diet.",
            "• Exercise at least 30 minutes daily.",
            "• Drink enough water.",
            "• Sleep 7–8 hours every night."
        ]
    elif category.lower() == "underweight":
        tips = [
            "• Eat more protein-rich foods.",
            "• Include healthy fats.",
            "• Strength training can help build muscle."
        ]
    elif category.lower() == "overweight":
        tips = [
            "• Reduce sugary foods.",
            "• Walk regularly.",
            "• Control portion sizes."
        ]
    else:
        tips = [
            "• Consult a healthcare professional.",
            "• Follow a balanced diet.",
            "• Exercise regularly."
        ]

    for tip in tips:
        story.append(Paragraph(tip, body_style))
    story.append(Spacer(1,0.2*inch))
    story.append(Paragraph("<b>Disclaimer</b>", styles["Heading3"]))

    story.append(
    Paragraph(
    "This report is for educational and informational purposes only. "
    "BMI is a screening measure, not a medical diagnosis. "
    "The water-intake figure is a simplified estimate, not a "
    "personalized prescription. Consult a qualified healthcare "
    "professional for individualized advice.",
    body_style
)
)

    story.append(
    Paragraph(
        "<hr width='100%'/>",
        body_style
    )
)

    story.append(
    Paragraph(
        "<b>Generated by:</b> FitTrack BMI",
        footer_style
    )
)

    story.append(
    Paragraph(
        "<i>Stay Healthy • Stay Fit</i>",
        footer_style
    )
)
    
    # Build the document
    doc.build(story)
    print("PDF Created Successfully")
    print(filename)
    return filename



