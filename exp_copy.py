import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red

def draw_frame(canvas, top_left, bottom_right):
    """
    Draws a red frame on the given canvas.

    Args:
        canvas: The ReportLab canvas object to draw on.
        top_left: Tuple (x1, y1) specifying the top-left corner of the frame.
        bottom_right: Tuple (x2, y2) specifying the bottom-right corner of the frame.
    """
    x1, y1 = top_left
    x2, y2 = bottom_right
    width = x2 - x1
    height = y2 - y1

    # Set the stroke color to red
    canvas.setStrokeColor(red)
    # Draw the rectangle
    canvas.rect(x1, y1, width, height, stroke=1, fill=0)  # No fill color needed

# Define the path to the template and output files
template_path = 'resources/petritek_template.pdf'
output_path = 'output_with_frame.pdf'

# Create a PdfReader object for the template
reader = PdfReader(template_path)
writer = PdfWriter()

# Create a canvas to draw on the template
packet = io.BytesIO()
c = canvas.Canvas(packet, pagesize=letter)

# Define top-left and bottom-right coordinates for the frame
top_left = (50, 710)  # Example top-left coordinates
bottom_right = (550, 80)  # Example bottom-right coordinates

# Draw the frame on the canvas
draw_frame(c, top_left, bottom_right)
c.save()

# Move the canvas data to the beginning of the file object
packet.seek(0)
new_pdf = PdfReader(packet)
existing_pdf = PdfReader(template_path)

# Add the "watermark" (which is the canvas with the red box) on the existing page
output = PdfWriter()
for i in range(len(existing_pdf.pages)):
    page = existing_pdf.pages[i]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

# Write the result to a file
with open(output_path, 'wb') as f:
    output.write(f)

print(f'Output saved to {output_path}')
