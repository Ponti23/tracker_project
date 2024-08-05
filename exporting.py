from reportlab.lib.pagesizes import letter
from PyQt5.QtWidgets import QFileDialog

def export_pdf(self):
    file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "PDF Files (*.pdf);;All Files (*)")
    print("saving file")
