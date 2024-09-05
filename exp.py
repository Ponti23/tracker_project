import io
import json
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(json_data, template_path, output_path):
    # Create a PdfReader object for the template
    reader = PdfReader(template_path)
    writer = PdfWriter()

    # Page 1: Print the file_name
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, json_data['file_name'])
    c.save()

    # Move the canvas data to the beginning of the file object
    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(template_path)
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    writer.add_page(page)

    # Page 2: Print the data
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 12)
    data_str = ','.join(map(str, json_data['data']))
    c.drawString(100, 750, data_str)
    c.save()

    # Move the canvas data to the beginning of the file object
    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(template_path)
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    writer.add_page(page)

    # Page 3: Print the date
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, json_data['date'])
    c.save()

    # Move the canvas data to the beginning of the file object
    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(template_path)
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    writer.add_page(page)

    # Write the result to a file
    with open(output_path, 'wb') as f:
        writer.write(f)

    print(f'Output saved to {output_path}')

# Example usage
json_data = {
    'file_name': 'TESTING NAME',
    'data': [0,1,0,0,0,2,6,7,25,7,6,2,1,0,0,0,1,0,0],
    'date': '31-12-9999'
}

create_pdf(json_data, 'resources/petritek_template.pdf', 'output_report.pdf')
