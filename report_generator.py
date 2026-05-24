from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def create_pdf(report_text, filename="research_report.pdf"):
    print(f"\n📄 Creating PDF: {filename}")
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.darkblue,
        spaceAfter=20
    )
    
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        leading=16,
        spaceAfter=10
    )
    
    story = []
    
    # Add title
    story.append(Paragraph("AI Research Report", title_style))
    story.append(Spacer(1, 20))
    
    # Add report content
    lines = report_text.split("\n")
    for line in lines:
        if line.strip():
            # Make headings bold
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")):
                heading_style = ParagraphStyle(
                    "Heading",
                    parent=styles["Normal"],
                    fontSize=13,
                    fontName="Helvetica-Bold",
                    textColor=colors.darkblue,
                    spaceAfter=8,
                    spaceBefore=12
                )
                story.append(Paragraph(line.strip(), heading_style))
            else:
                # Clean special characters
                clean_line = line.strip()
                clean_line = clean_line.replace("&", "&amp;")
                clean_line = clean_line.replace("<", "&lt;")
                clean_line = clean_line.replace(">", "&gt;")
                story.append(Paragraph(clean_line, body_style))
            
            story.append(Spacer(1, 4))
    
    doc.build(story)
    print(f"✅ PDF saved as: {filename}")
    return filename