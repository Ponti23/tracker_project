from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from PIL import Image as PilImage
import json
from datetime import datetime

def add_header_footer(canvas, doc):
    canvas.saveState()

    header_image_path = 'resources/header.png'
    footer_image_path = 'resources/footer.png'

    header_image = PilImage.open(header_image_path)
    footer_image = PilImage.open(footer_image_path)

    header_width, header_height = header_image.size
    footer_width, footer_height = footer_image.size

    aspect_ratio_header = header_width / header_height
    aspect_ratio_footer = footer_width / footer_height

    doc_width, doc_height = doc.pagesize

    scaled_header_height = 2.5 * inch
    scaled_header_width = scaled_header_height * aspect_ratio_header

    scaled_footer_height = 2.5 * inch
    scaled_footer_width = scaled_footer_height * aspect_ratio_footer

    if scaled_header_width > doc_width:
        scaled_header_width = doc_width
        scaled_header_height = scaled_header_width / aspect_ratio_header

    if scaled_footer_width > doc_width:
        scaled_footer_width = doc_width
        scaled_footer_height = scaled_footer_width / aspect_ratio_footer

    canvas.drawImage(header_image_path, (doc_width - scaled_header_width) / 2,
                     doc_height - scaled_header_height,
                     width=scaled_header_width, height=scaled_header_height)

    canvas.drawImage(footer_image_path, (doc_width - scaled_footer_width) / 2,
                     0,
                     width=scaled_footer_width, height=scaled_footer_height)

    canvas.restoreState()

def create_pdf(json_data, output_filename="report.pdf"):
    doc = BaseDocTemplate(output_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    content = []

    header_height = 2.5 * inch
    footer_height = 2.5 * inch

    frame = Frame(doc.leftMargin, doc.bottomMargin + footer_height,
                  doc.width, doc.height - header_height - footer_height,
                  id='frame')

    template = PageTemplate(id='my_template', frames=[frame], onPage=add_header_footer)
    doc.addPageTemplates([template])

    # Page 1: Title Page
    title_style = styles['Title']
    normal_style = styles['Normal']

    current_date_time = datetime.now().strftime("%A, %d %B %Y %H:%M:%S")

    content.append(Spacer(1, 2 * inch))  # Adjust spacer for vertical alignment
    content.append(Paragraph("Data Report for " + json_data['file_name'], title_style))
    content.append(Spacer(1, 12))  # Space between title and line
    content.append(Paragraph("Current Date & Time:", normal_style))
    content.append(Paragraph(current_date_time, normal_style))
    content.append(Spacer(1, 24))  # Space before page break

    # Page 2: Print JSON content
    json_str = json.dumps(json_data, indent=4)
    content.append(Paragraph("JSON CONTENT:", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(json_str, styles['Normal']))
    content.append(PageBreak())

    doc.build(content)

# Example usage
json_data = {
    'file_name': 'TEST_2_PEAKS.CSV',
    'date_start': '07-01-24',
    'time_start': '00:00:00',
    'date_end': '23-01-24',
    'time_end': '16:36:43',
    'calibration_factor': '00000',
    'tube_voltage': '00780',
    'recording_elapsed': '15.85832175925926',
    'total_peak': '3',
    'peak_data': [
        {'index': 1446106, 'date': '12-01-24', 
         'time': '00:26:11', 
         'x-axis': [1446096, 1446097, 1446098, 1446099, 1446100, 
                    1446101, 1446102, 1446103, 1446104, 1446105, 
                    1446106, 1446107, 1446108, 1446109, 1446110, 
                    1446111, 1446112, 1446113, 1446114, 1446115, 
                    1446116, 1446117, 1446118, 1446119, 1446120], 
        'y-axis': [1, 0, 1, 0, 3, 2, 1, 13, 39, 134, 522, 1247, 
                   1082, 437, 109, 22, 4, 3, 2, 0, 3, 0, 1, 4, 0]}, 
                   
        {'index': 3489549, 
         'date': '17-01-24', 
         'time': '22:20:32', 
         'x-axis': [3489539, 3489540, 3489541, 3489542, 3489543, 
                    3489544, 3489545, 3489546, 3489547, 3489548, 
                    3489549, 3489550, 3489551, 3489552, 3489553, 
                    3489554, 3489555, 3489556, 3489557, 3489558, 
                    3489559, 3489560, 3489561, 3489562, 3489563], 
                    
            'y-axis': [2, 0, 0, 0, 1, 2, 9, 15, 29, 101, 309, 699, 
                       753, 470, 228, 54, 22, 9, 4, 2, 4, 1, 3, 0, 3]}, 
                       
        {'index': 5134971, 
         'date': '22-01-24', 
         'time': '16:36:27', 
         'x-axis': [5134961, 5134962, 5134963, 5134964, 5134965, 
                    5134966, 5134967, 5134968, 5134969, 5134970, 
                    5134971, 5134972, 5134973, 5134974, 5134975, 
                    5134976, 5134977, 5134978, 5134979, 5134980, 
                    5134981, 5134982, 5134983, 5134984, 5134985], 
                    
        'y-axis': [1, 0, 1, 0, 3, 2, 1, 13, 39, 134, 522, 1247, 
                   1082, 437, 109, 22, 4, 3, 2, 0, 3, 0, 1, 4, 0]
        }],

    'raw_data': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10000000,100000000,100000000000,100000000,10000000,0,0,0,0,0,0,00,0,0,0],
    'background_data': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10000,100000,100000000,100000,10000,0,0,0,0,0,0,0,0,0,0],
    'threshold': [10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,1000000,10000000,10000000000,10000000,1000000,10,10,10,10,10,10,10,10,10,10],
}

create_pdf(json_data)
