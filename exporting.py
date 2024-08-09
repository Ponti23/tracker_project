from docx import Document

def modify_template(template_path, text_to_insert, output_file_path):
    # Open the .docx file
    doc = Document(template_path)
    print(template_path)

    # Insert text at the end of the document
    doc.add_paragraph(text_to_insert)
    print(text_to_insert)

    # Save the changes to a new document
    doc.save(output_file_path)
    print(output_file_path)

# Example usage
template_path = r"C:\A_Temporary\tracker_project\petritek_template.docx"  # Replace with your template path
text_to_insert = "This is the text to insert into the .docx file."  # Text to be added
output_file_path = r"C:\A_Temporary\tracker_project\modified_template.docx"  # Path to save the new file

modify_template(template_path, text_to_insert, output_file_path)
