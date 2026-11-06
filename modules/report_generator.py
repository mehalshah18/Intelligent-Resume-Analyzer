
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO


def generate_pdf_report(results, job_title):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    content = []

    content.append(
        Paragraph("Intelligent Resume Analyzer Report",
                  styles["Title"])
    )
    content.append(Spacer(1, 15))

    content.append(
        Paragraph(f"Job Title: {job_title}", styles["Heading2"])
    )
    content.append(Spacer(1, 12))

    final_score = results.get("final_score", 0)

    content.append(
        Paragraph(
            f"Overall Resume Match Score: {final_score}%",
            styles["Heading2"]
        )
    )
    content.append(Spacer(1, 15))

    content.append(
        Paragraph("Individual Evaluation Scores",
                  styles["Heading2"])
    )

    score_data = [["Category", "Score"]]

    for category, score in results.get(
        "individual_scores", {}
    ).items():
        display_score = (
            "Not evaluated" if score is None
            else f"{score}%"
        )
        score_data.append([category.title(), display_score])

    table = Table(score_data, colWidths=[3 * inch, 2 * inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#264653")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    content.append(table)
    content.append(Spacer(1, 20))

    explanation = results.get("explanation", {})

    for heading, key in [
        ("Strengths", "strengths"),
        ("Areas for Improvement", "improvements")
    ]:
        content.append(
            Paragraph(heading, styles["Heading2"])
        )

        for item in explanation.get(key, []):
            safe_item = (
                str(item)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            content.append(
                Paragraph(safe_item, styles["BodyText"])
            )
            content.append(Spacer(1, 5))

        content.append(Spacer(1, 10))

    document.build(content)

    buffer.seek(0)
    return buffer.getvalue()
