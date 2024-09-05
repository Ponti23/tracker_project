import streamlit as st
import pandas as pd

# Function to open a CSV file
def open_csv(uploaded_file):
    document_information = {}
    try:
        # Read the CSV file directly from the UploadedFile object
        document_information = pd.read_csv(uploaded_file).to_dict(orient='list')
    except Exception as e:
        st.error(f"Error opening file: {e}")
    return document_information

# Streamlit app
st.title("CSV File Viewer")

# Upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Get the document information from the CSV
    document_information = open_csv(uploaded_file)

    # Print out the contents of self.document_information
    st.subheader("Contents of the CSV File (self.document_information)")
    st.write(document_information)
