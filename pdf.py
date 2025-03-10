from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

class Pdf():
    @staticmethod
    def generate_homework_pdf(student_name, topic, date, homework_text):
        # 🏠 Define base directory for all homework PDFs
        base_dir = "homework_pdfs"  
        os.makedirs(base_dir, exist_ok=True)  # Create if not exists

        # 📂 Define student folder
        student_dir = os.path.join(base_dir, student_name.replace(" ", "_"))  # Replace spaces in name
        os.makedirs(student_dir, exist_ok=True)  # Create student's folder if not exists

        # 📄 Define file name: "<student_name>_<topic>_<date>.pdf"
        date_str = date.strftime("%Y-%m-%d")  # Format date as YYYY-MM-DD
        file_name = f"{topic.replace(' ', '_')}_{date_str}_{student_name.replace(' ', '_')}.pdf"
        pdf_path = os.path.join(student_dir, file_name)

        # 📝 Generate PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        # 🏫 Add student info
        c.drawString(100, 750, f"Schüler: {student_name}")
        c.drawString(100, 730, f"Thema: {topic}")
        c.drawString(100, 710, f"Datum: {date_str}")

        # ✍️ Add homework text
        c.drawString(100, 680, "Hausaufgabe:")
        text_object = c.beginText(100, 660)
        text_object.setFont("Helvetica", 10)
        
        # Wrap text into multiple lines
        for line in homework_text.split("\n"):
            text_object.textLine(line)
        
        c.drawText(text_object)

        # 📌 Save the PDF
        c.save()

        print(f"✅ PDF saved successfully: {pdf_path}")
