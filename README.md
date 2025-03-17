# PDF Converter

A streamlined Streamlit application that converts text or markdown content into simple PDF documents optimized for LLM processing. The focus is on preserving content and structure rather than visual aesthetics.

## Features

- Text area for entering or pasting content
- Option to upload a markdown or text file
- Support for basic markdown syntax (headings, lists, paragraphs)
- Convert text/markdown to PDF with minimal formatting
- Preserve text content and basic structure
- Download the generated PDF

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd pdf-converter
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL displayed in the terminal (typically http://localhost:8501)

3. Enter text or markdown content in the text area, or upload a markdown/text file

4. Click the "Generate PDF" button

5. Download the generated PDF using the download button

## Project Structure

```
pdf-converter/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
└── utils/
    ├── text_processor.py   # Basic text/markdown processing
    └── pdf_generator.py    # Simple PDF generation
``` 