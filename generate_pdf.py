from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import json

def generate_pdf(text_summary, table_json_path, output_path="video_analysis_report.pdf"):

    # Load table data (detections_summary.json)
    data = json.load(open(table_json_path, "r"))

    # Convert dict to list for table format
    table_data = [["Person ID", "Entry", "Exit", "Direction", "Speed"]]

    for pid, info in data.items():
        table_data.append([
            str(info["person_id"]),
            str(info["entry_frame"]),
            str(info["exit_frame"]),
            str(info.get("dominant_direction", "unknown")),
            str(info.get("avg_speed", "unknown"))
        ])

    # PDF Setup
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>Video Analysis Report</b>", styles["Title"]))
    story.append(Spacer(1, 20))

    # Text Summary Section
    story.append(Paragraph("<b>Summary</b>", styles["Heading2"]))
    for line in text_summary.split("\n"):
        story.append(Paragraph(line, styles["BodyText"]))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # Table Section Title
    story.append(Paragraph("<b>Person-wise Table</b>", styles["Heading2"]))
    story.append(Spacer(1, 10))

    # Create Table
    t = Table(table_data, colWidths=[70, 70, 70, 90, 90])

    # Style Table
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1a73e8")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ])

    t.setStyle(style)
    story.append(t)

    doc.build(story)
    print(f"📄 PDF created: {output_path}")


# ==========================================================
# MAIN EXECUTION
# ==========================================================
if __name__ == "__main__":
    # Read the LLM summary
    text = open("analysis.txt", "r", encoding="utf-8").read()

    # Path to detections_summary.json
    table_json_path = "detections_summary.json"

    generate_pdf(text, table_json_path)
