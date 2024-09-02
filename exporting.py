from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageTemplate, BaseDocTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

def create_graph(x_data, y_data, title):
    fig = Figure(figsize=(6, 3))
    ax = fig.add_subplot(111)
    ax.plot(x_data, y_data, marker='o', linestyle='-', color='b')
    ax.set_title(f"Peak at index {title}")
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.grid(True)

    buffer = BytesIO()
    FigureCanvas(fig).print_png(buffer)
    buffer.seek(0)

    return buffer

def add_header_footer(canvas, doc):
    canvas.saveState()
    
    header_image_path = 'resources/header.png'
    footer_image_path = 'resources/footer.png'
    
    header_height = 2.5 * inch
    footer_height = 2.5 * inch
    
    header_width = doc.pagesize[0]
    footer_width = doc.pagesize[0]
    
    canvas.drawImage(header_image_path, 0, doc.pagesize[1] - header_height, 
                     width=header_width, height=header_height, 
                     preserveAspectRatio=False)
    
    canvas.drawImage(footer_image_path, 0, 0, 
                     width=footer_width, height=footer_height, 
                     preserveAspectRatio=False)

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
    
    content.append(Paragraph(f"File Name: {json_data['file_name']}", styles['Normal']))
    content.append(Paragraph(f"Date Start: {json_data['date_start']}", styles['Normal']))
    content.append(Paragraph(f"Date End: {json_data['date_end']}", styles['Normal']))
    content.append(Paragraph(f"Time End: {json_data['time_end']}", styles['Normal']))
    content.append(Paragraph(f"Calibration Factor: {json_data['calibration_factor']}", styles['Normal']))
    content.append(Paragraph(f"Tube Voltage: {json_data['tube_voltage']}", styles['Normal']))
    content.append(Paragraph(f"Recording Elapsed: {json_data['recording_elapsed']}", styles['Normal']))
    content.append(Paragraph(f"Total Peaks Detected: {json_data['total_peak']}", styles['Normal']))
    content.append(Spacer(1, 0.2 * inch))

    for peak in json_data['peak_data']:
        peak_index = peak['index']
        peak_date = peak['date']
        peak_time = peak['time']
        x_data = peak['x-axis']
        y_data = peak['y-axis']

        content.append(Paragraph(f"Peak Index: {peak_index}", styles['Heading2']))
        content.append(Paragraph(f"Date of Peak: {peak_date}", styles['Normal']))
        content.append(Paragraph(f"Time of Peak: {peak_time}", styles['Normal']))
        graph_buffer = create_graph(x_data, y_data, peak_index)
        graph_image = Image(graph_buffer, 6 * inch, 3 * inch)
        content.append(graph_image)
        content.append(Spacer(1, 0.2 * inch))

    doc.build(content)
