from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image as PILImage
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_graph_image(x_axis, y_axis, filename):
    plt.figure(figsize=(6, 3))
    plt.plot(x_axis, y_axis, marker='o')
    plt.title('Peak Data')
    plt.grid(True)
    
    # Hide x and y axis labels
    plt.xlabel('')
    plt.ylabel('')
    
    # Save the figure with tight bounding box
    plt.savefig(filename, bbox_inches='tight', pad_inches=0.1)
    plt.close()

def add_header_footer(canvas, doc):
    # Header and Footer image paths
    header_image_path = 'resources/header.png'
    footer_image_path = 'resources/footer.png'
    
    # Define sizes for header and footer
    
    header_width = doc.pagesize[0]  # Full page width
    header_height = 2.5 * inch     # Adjust height as needed
    
    footer_width = doc.pagesize[0]  # Full page width
    footer_height = 2.5 * inch     # Adjust height as needed
    
    # Add Header
    canvas.drawImage(header_image_path, 0, doc.pagesize[1] - header_height, 
                     width=header_width, height=header_height, 
                     preserveAspectRatio=False)
    
    # Add Footer
    canvas.drawImage(footer_image_path, 0, 0, 
                     width=footer_width, height=footer_height, 
                     preserveAspectRatio=False)

def generate_pdf(data, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    content = []

    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    # Add a title
    content.append(Paragraph("Peak Data Report", title_style))

    # Add data information
    info_table_data = [
        ['File Name:', data['file_name']],
        ['Date Start:', data['date_start']],
        ['Date End:', data['date_end']],
        ['Time End:', data['time_end']],
        ['Calibration Factor:', data['calibration_factor']],
        ['Tube Voltage:', data['tube_voltage']],
        ['Recording Elapsed:', data['recording_elapsed']],
        ['Total Peaks:', data['total_peak']],
    ]

    info_table = Table(info_table_data, colWidths=[150, 300])  # Adjust column widths
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('WORDWRAP', (0, 1), (-1, -1), 'CJK'),
    ]))

    content.append(info_table)

    # Add peak data plots
    for i, peak in enumerate(data['peak_data']):
        x_axis = peak['x-axis']
        y_axis = peak['y-axis']
        
        # Save the plot to an image file
        image_filename = f"peak_plot_{i}.png"
        create_graph_image(x_axis, y_axis, image_filename)
        
        # Add image to the PDF
        with open(image_filename, 'rb') as img_file:
            img = PILImage.open(img_file)
            image_buffer = BytesIO()
            img.save(image_buffer, format='PNG')
            image_buffer.seek(0)
            content.append(Paragraph(f"Peak {i+1}:", normal_style))
            # Preserve aspect ratio when adding to PDF
            img_width, img_height = img.size
            aspect_ratio = img_height / img_width
            content.append(Image(image_buffer, width=6*inch, height=6*inch*aspect_ratio))

    # Build the PDF with custom header and footer
    doc.build(content, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
"""
# Example usage
json_data = {
    'file_name': 'example_file.csv',
    'date_start': '2024-01-01',
    'date_end': '2024-01-31',
    'time_end': '23:59:59',
    'calibration_factor': '0.123',
    'tube_voltage': '5.0V',
    'recording_elapsed': '30 days',
    'total_peak': '5',
    'peak_data': [
        {'index': 1446106, 
         'x-axis': [1446096, 1446097, 1446098, 1446099, 1446100, 1446101, 1446102, 1446103, 1446104, 1446105, 1446106, 1446107, 1446108, 1446109, 1446110, 1446111, 1446112, 1446113, 1446114, 1446115, 1446116, 1446117, 1446118, 1446119, 1446120], 
         'y-axis': [1, 0, 1, 0, 3, 2, 1, 13, 39, 134, 522, 1247, 1082, 437, 109, 22, 4, 3, 2, 0, 3, 0, 1, 4, 0]
        },
        {'index': 3489549, 
         'x-axis': [3489539, 3489540, 3489541, 3489542, 3489543, 3489544, 3489545, 3489546, 3489547, 3489548, 3489549, 3489550, 3489551, 3489552, 3489553, 3489554, 3489555, 3489556, 3489557, 3489558, 3489559, 3489560, 3489561, 3489562, 3489563], 
         'y-axis': [2, 0, 0, 0, 1, 2, 9, 15, 29, 101, 309, 699, 753, 470, 228, 54, 22, 9, 4, 2, 4, 1, 3, 0, 3]
        },
        {'index': 5134971, 
         'x-axis': [5134961, 5134962, 5134963, 5134964, 5134965, 5134966, 5134967, 5134968, 5134969, 5134970, 5134971, 5134972, 5134973, 5134974, 5134975, 5134976, 5134977, 5134978, 5134979, 5134980, 5134981, 5134982, 5134983, 5134984, 5134985], 
         'y-axis': [1, 0, 1, 0, 3, 2, 1, 13, 39, 134, 522, 1247, 1082, 437, 109, 22, 4, 3, 2, 0, 3, 0, 1, 4, 0]
        }
    ]
}

generate_pdf(json_data, 'Peak_Data_Report.pdf')
"""