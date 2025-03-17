"""
PDF generator utility for converting text/markdown to PDF.
"""
import os
import tempfile
import re
from fpdf import FPDF
from typing import Dict, List, Any, Optional

class PDFGenerator:
    """
    Class for generating PDFs from text or markdown content.
    """
    def __init__(self):
        """Initialize the PDF generator."""
        # Create PDF with Unicode support
        self.pdf = FPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        
        # Use a standard font
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
        
        # Define character replacements for problematic symbols
        self.char_replacements = {
            '•': '-',  # Replace bullet points with hyphens
            '–': '-',  # Replace en dash with hyphen
            '—': '-',  # Replace em dash with hyphen
            ''': "'",  # Replace smart quotes
            ''': "'",
            '"': '"',
            '"': '"',
            '…': '...',  # Replace ellipsis
            '≤': '<=',
            '≥': '>=',
            '©': '(c)',
            '®': '(R)',
            '™': '(TM)',
            '°': ' degrees',
            '±': '+/-',
            '×': 'x',
            '÷': '/',
            '½': '1/2',
            '¼': '1/4',
            '¾': '3/4',
            # Add more replacements as needed
        }
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitize text by replacing problematic characters.
        
        Args:
            text (str): Text to sanitize
            
        Returns:
            str: Sanitized text
        """
        # Replace known problematic characters
        for char, replacement in self.char_replacements.items():
            text = text.replace(char, replacement)
        
        # Replace any remaining non-ASCII characters with their closest ASCII equivalent or a placeholder
        sanitized_text = ''
        for char in text:
            if ord(char) < 128:  # ASCII characters
                sanitized_text += char
            else:
                # Try to find a close ASCII equivalent or use a placeholder
                sanitized_text += self.char_replacements.get(char, ' ')
        
        return sanitized_text
    
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
        
        # Sanitize text to handle special characters
        safe_text = self.sanitize_text(text)
        
        try:
            self.pdf.cell(0, 10, safe_text, ln=True)
        except Exception as e:
            # Fall back to a simpler representation if any error occurs
            self.pdf.cell(0, 10, f"Heading level {level}", ln=True)
            print(f"Error rendering heading: {e}")
            
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
        
        # Sanitize text to handle special characters
        safe_text = self.sanitize_text(text)
        
        try:
            self.pdf.multi_cell(0, 10, safe_text)
        except Exception as e:
            # Fall back to a simpler representation if any error occurs
            self.pdf.multi_cell(0, 10, "[Text contains unsupported characters]")
            print(f"Error rendering paragraph: {e}")
            
        self.pdf.ln(5)
    
    def add_list(self, items: List[str]):
        """
        Add a list to the PDF.
        
        Args:
            items (List[str]): List items
        """
        self.pdf.set_font("Arial", size=12)
        for item in items:
            # Use a simple hyphen instead of bullet point
            self.pdf.cell(10, 10, "-", ln=0)
            
            # Sanitize text to handle special characters
            safe_item = self.sanitize_text(item)
            
            try:
                self.pdf.multi_cell(0, 10, safe_item)
            except Exception as e:
                # Fall back to a simpler representation if any error occurs
                self.pdf.multi_cell(0, 10, "[Item contains unsupported characters]")
                print(f"Error rendering list item: {e}")
    
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
        # Sanitize text to handle special characters
        safe_text = self.sanitize_text(text)
        
        try:
            self.pdf.multi_cell(0, 10, safe_text)
        except Exception as e:
            # Fall back to a simpler representation if any error occurs
            self.pdf.multi_cell(0, 10, "[Text contains unsupported characters]")
            print(f"Error rendering text: {e}")
    
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
        
        try:
            self.pdf.output(output_path)
        except Exception as e:
            print(f"Error generating PDF: {e}")
            # If there's an error, create a simple error PDF
            error_pdf = FPDF()
            error_pdf.add_page()
            error_pdf.set_font("Arial", size=12)
            error_pdf.cell(0, 10, "Error generating PDF with the provided content.", ln=True)
            error_pdf.cell(0, 10, "The content may contain unsupported characters.", ln=True)
            error_pdf.output(output_path)
            
        return output_path 