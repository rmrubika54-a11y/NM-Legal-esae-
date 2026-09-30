from flask import Flask, render_template, request, send_file
from io import BytesIO
from reportlab.pdfgen import canvas

app = Flask(__name__)

DOCUMENT_TEMPLATES = {
    "Rental Agreement": """RENTAL AGREEMENT

This agreement is prepared for {name}.

Purpose:
{purpose}

Date: {date}

The parties agree to follow the terms mentioned in this document.

Signature: __________________
""",
    "Affidavit": """AFFIDAVIT

I, {name}, hereby state that the information provided for the following purpose is true to the best of my knowledge.

Purpose:
{purpose}

Date: {date}

Signature: __________________
""",
    "Authorization Letter": """AUTHORIZATION LETTER

I, {name}, authorize the concerned person/authority for the following purpose:

{purpose}

Date: {date}

Signature: __________________
""",
    "Employment Agreement": """EMPLOYMENT AGREEMENT

Employee Name: {name}

Purpose / Employment Details:
{purpose}

Date: {date}

Employee Signature: __________________
Employer Signature: __________________
"""
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name", "")
    document_type = request.form.get("document_type", "Rental Agreement")
    purpose = request.form.get("purpose", "")
    date = request.form.get("date", "")

    template = DOCUMENT_TEMPLATES.get(document_type, DOCUMENT_TEMPLATES["Rental Agreement"])
    document = template.format(name=name, purpose=purpose, date=date)

    return render_template("index.html", document=document)

@app.route("/download", methods=["POST"])
def download():
    document = request.form.get("document", "")
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setTitle("Legal Ease Generated Document")

    y = 800
    for line in document.splitlines():
        pdf.drawString(50, y, line[:100])
        y -= 18
        if y < 50:
            pdf.showPage()
            y = 800

    pdf.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True,
                     download_name="Legal_Ease_Document.pdf",
                     mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
