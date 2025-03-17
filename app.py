"""
PDF Converter - A Streamlit app to convert text/markdown to PDF.
"""
import os
import streamlit as st
import tempfile
import base64
from utils.text_processor import parse_markdown, extract_structure, process_text
from utils.pdf_generator import PDFGenerator

# Set page configuration
st.set_page_config(
    page_title="PDF Converter",
    page_icon="📄",
    layout="wide"
)

def get_binary_file_downloader_html(bin_file, file_label='File', custom_filename=None):
    """
    Generate a download link for a binary file.
    
    Args:
        bin_file (str): Path to the binary file
        file_label (str): Label for the file
        custom_filename (str, optional): Custom filename for download
        
    Returns:
        str: HTML for the download link
    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    download_filename = custom_filename if custom_filename else os.path.basename(bin_file)
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{download_filename}">{file_label}</a>'

def main():
    """Main function to run the Streamlit app."""
    st.title("PDF Converter")
    st.markdown("""
    Convert text or markdown content into simple PDF documents optimized for LLM processing.
    The focus is on preserving content and structure rather than visual aesthetics.
    """)
    
    # Add a section for PDF options
    st.subheader("PDF Options")
    col1, col2 = st.columns(2)
    
    with col1:
        pdf_filename = st.text_input("PDF Filename (optional)", value="output.pdf")
    
    with col2:
        st.markdown("PDF is optimized for LLM processing with minimal formatting.")
    
    # Create tabs for different input methods
    tab1, tab2 = st.tabs(["Text Input", "File Upload"])
    
    with tab1:
        # Text input area
        text_input = st.text_area(
            "Enter your text or markdown content here:",
            height=300,
            placeholder="# Your Markdown Content\n\nEnter your content here. You can use markdown formatting like **bold**, *italic*, or lists:\n\n- Item 1\n- Item 2\n\n## Second Heading\n\nMore content..."
        )
        
        # Options for text input
        is_markdown = st.checkbox("This is markdown content", value=True)
        
        # Generate PDF button for text input
        if st.button("Generate PDF from Text", key="generate_text"):
            if text_input:
                with st.spinner("Generating PDF..."):
                    # Process the text based on whether it's markdown or plain text
                    pdf_generator = PDFGenerator()
                    
                    if is_markdown:
                        # Extract structure from markdown
                        structure = extract_structure(text_input)
                        pdf_generator.add_content_from_structure(structure)
                    else:
                        # Process plain text
                        processed_text = process_text(text_input)
                        pdf_generator.add_text(processed_text)
                    
                    # Generate the PDF with the custom filename
                    temp_pdf_path = pdf_generator.generate_pdf()
                    
                    # Display download link with custom filename
                    st.success("PDF generated successfully!")
                    st.markdown(
                        get_binary_file_downloader_html(temp_pdf_path, 'Download PDF', pdf_filename),
                        unsafe_allow_html=True
                    )
            else:
                st.error("Please enter some text or markdown content.")
    
    with tab2:
        # File upload
        uploaded_file = st.file_uploader("Upload a text or markdown file", type=["txt", "md"])
        
        if uploaded_file is not None:
            # Read the file content
            file_content = uploaded_file.read().decode("utf-8")
            
            # Display the file content
            st.subheader("File Content Preview:")
            st.text_area("", file_content, height=200)
            
            # Determine if the file is markdown based on extension
            file_extension = uploaded_file.name.split(".")[-1].lower()
            is_file_markdown = file_extension == "md"
            
            # Option to override the file type detection
            is_file_markdown = st.checkbox(
                "This is markdown content",
                value=is_file_markdown
            )
            
            # Generate PDF button for file upload
            if st.button("Generate PDF from File", key="generate_file"):
                with st.spinner("Generating PDF..."):
                    # Process the file content
                    pdf_generator = PDFGenerator()
                    
                    if is_file_markdown:
                        # Extract structure from markdown
                        structure = extract_structure(file_content)
                        pdf_generator.add_content_from_structure(structure)
                    else:
                        # Process plain text
                        processed_text = process_text(file_content)
                        pdf_generator.add_text(processed_text)
                    
                    # Use the custom filename if provided, otherwise use the original filename
                    if pdf_filename == "output.pdf":
                        download_filename = f"{os.path.splitext(uploaded_file.name)[0]}.pdf"
                    else:
                        download_filename = pdf_filename
                    
                    # Generate the PDF
                    temp_pdf_path = pdf_generator.generate_pdf()
                    
                    # Display download link with custom filename
                    st.success("PDF generated successfully!")
                    st.markdown(
                        get_binary_file_downloader_html(temp_pdf_path, 'Download PDF', download_filename),
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main() 