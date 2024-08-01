from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
import os
import tempfile

def export_file(ui_instance):
    file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "PDF Files (*.pdf);;All Files (*)")

    if file_path:
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Add text data
        c.drawString(100, height - 100, f"File Name: {ui_instance.data_information['file_name']}")
        c.drawString(100, height - 120, f"Start Date: {ui_instance.data_information['date_start']}")
        c.drawString(100, height - 140, f"Start Time: {ui_instance.data_information['time_start']}")
        c.drawString(100, height - 160, f"End Date: {ui_instance.data_information['date_end']}")
        c.drawString(100, height - 180, f"End Time: {ui_instance.data_information['time_end']}")
        c.drawString(100, height - 200, f"Calibration Factor: {ui_instance.data_information['calibration_factor']}")
        c.drawString(100, height - 220, f"Tube Voltage: {ui_instance.data_information['tube_voltage']}")

        # Add peak data information
        c.drawString(100, height - 240, f"Peak Amount: {ui_instance.peak_amount_text.text()}")
        c.drawString(100, height - 260, f"Peak Date: {ui_instance.peak_date_text.text()}")
        c.drawString(100, height - 280, f"Peak Time: {ui_instance.peak_time_text.text()}")
        c.drawString(100, height - 300, f"Peak Value: {ui_instance.peak_value_text.text()}")

        # Save raw data plot as an image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            raw_data_image_path = temp_file.name
            ui_instance.raw_data_figure.savefig(raw_data_image_path, format='png')
            c.drawImage(raw_data_image_path, 100, height - 500, width=4*inch, height=3*inch)
        
        # Save peak data plot as an image
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_file:
            peak_data_image_path = temp_file.name
            ui_instance.peak_data_figure.savefig(peak_data_image_path, format='png')
            c.drawImage(peak_data_image_path, 100, height - 900, width=4*inch, height=3*inch)

        c.save()

        # Clean up temporary files
        os.remove(raw_data_image_path)
        os.remove(peak_data_image_path)
