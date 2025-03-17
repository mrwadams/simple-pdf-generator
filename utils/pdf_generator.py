"""
PDF generator utility for converting text/markdown to PDF.
"""
import os
import tempfile
from fpdf import FPDF
from typing import Dict, List, Any, Optional

class PDFGenerator:
    """
    Class for generating PDFs from text or markdown content.
    """
    def __init__(self):
        """Initialize the PDF generator."""
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        
        # Add a Unicode font (DejaVu) which has better character support
        self.pdf.add_page()
        
        # Use a font with better Unicode support
        # Default to built-in fonts which should work across platforms
        self.pdf.set_font("Arial", size=12)
        
        # Define font sizes for different heading levels
        self.heading_sizes = {
            1: 24,
            2: 20,
            3: 16,
            4: 14,
            5: 12,
            6: 12
        }
    
    def add_heading(self, text: str, level: int = 1):
        """
        Add a heading to the PDF.
        
        Args:
            text (str): Heading text
            level (int): Heading level (1-6)
        """
        # Set font size based on heading level
        size = self.heading_sizes.get(level, 12)
        self.pdf.set_font("Arial", "B", size=size)
        self.pdf.ln(10)
        
        # Handle potential encoding issues
        try:
            self.pdf.cell(0, 10, text, ln=True)
        except UnicodeEncodeError:
            # Fall back to a simpler representation if encoding fails
            self.pdf.cell(0, 10, f"Heading level {level}", ln=True)
            
        self.pdf.ln(5)
        # Reset to normal font
        self.pdf.set_font("Arial", size=12)
    
    def add_paragraph(self, text: str):
        """
        Add a paragraph to the PDF.
        
        Args:
            text (str): Paragraph text
        """
        self.pdf.set_font("Arial", size=12)
        
        # Handle potential encoding issues
        try:
            self.pdf.multi_cell(0, 10, text)
        except UnicodeEncodeError:
            # Fall back to a simpler representation if encoding fails
            self.pdf.multi_cell(0, 10, "[Text contains unsupported characters]")
            
        self.pdf.ln(5)
    
    def add_list(self, items: List[str]):
        """
        Add a list to the PDF.
        
        Args:
            items (List[str]): List items
        """
        self.pdf.set_font("Arial", size=12)
        for item in items:
            self.pdf.cell(10, 10, "•", ln=0)
            
            # Handle potential encoding issues
            try:
                self.pdf.multi_cell(0, 10, item)
            except UnicodeEncodeError:
                # Fall back to a simpler representation if encoding fails
                self.pdf.multi_cell(0, 10, "[Item contains unsupported characters]")
    
    def add_content_from_structure(self, structure: Dict[str, Any]):
        """
        Add content to the PDF based on the extracted structure.
        
        Args:
            structure (Dict[str, Any]): Structure information
        """
        # Add headings
        for heading in structure['headings']:
            self.add_heading(heading['text'], heading['level'])
        
        # Add paragraphs
        for paragraph in structure['paragraphs']:
            self.add_paragraph(paragraph)
        
        # Add lists
        for list_items in structure['lists']:
            self.add_list(list_items)
    
    def add_text(self, text: str):
        """
        Add plain text to the PDF.
        
        Args:
            text (str): Text to add
        """
        # Handle potential encoding issues
        try:
            self.pdf.multi_cell(0, 10, text)
        except UnicodeEncodeError:
            # Fall back to a simpler representation if encoding fails
            self.pdf.multi_cell(0, 10, "[Text contains unsupported characters]")
    
    def generate_pdf(self, output_path: Optional[str] = None) -> str:
        """
        Generate the PDF file.
        
        Args:
            output_path (Optional[str]): Path to save the PDF file
            
        Returns:
            str: Path to the generated PDF file
        """
        if output_path is None:
            # Create a temporary file
            fd, output_path = tempfile.mkstemp(suffix='.pdf')
            os.close(fd)
        
        self.pdf.output(output_path)
        return output_path 