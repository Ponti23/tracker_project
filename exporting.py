from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def export_pdf(data_information, raw_data, file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    # Set up font and size
    c.setFont("Helvetica", 12)

    # Write data to PDF
    y_position = height - 50  # Starting Y position on the page

    # Add file information
    if data_information:  # Ensure data_information is populated
        c.drawString(50, y_position, f"File Name: {data_information['file_name']}")
        y_position -= 20
        c.drawString(50, y_position, f"Date Start: {data_information['date_start']}")
        y_position -= 20
        c.drawString(50, y_position, f"Time Start: {data_information['time_start']}")
        y_position -= 20
        c.drawString(50, y_position, f"Date End: {data_information['date_end']}")
        y_position -= 20
        c.drawString(50, y_position, f"Time End: {data_information['time_end']}")
        y_position -= 20
        c.drawString(50, y_position, f"Calibration Factor: {data_information['calibration_factor']}")
        y_position -= 20
        c.drawString(50, y_position, f"Tube Voltage: {data_information['tube_voltage']}")
        y_position -= 20

    # Add graph data if needed
    if raw_data:
        c.drawString(50, y_position, "Raw Data:")
        y_position -= 20
        for i, value in enumerate(raw_data[:10]):  # Just an example to show first 10 points
            c.drawString(50, y_position, f"Point {i+1}: {value}")
            y_position -= 20

    # Save the PDF file
    c.save()
