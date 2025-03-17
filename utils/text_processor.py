"""
Text processor utility for handling markdown parsing.
"""
import markdown
from typing import Dict, Any


def parse_markdown(text: str) -> str:
    """
    Parse markdown text to HTML.
    
    Args:
        text (str): Markdown text to parse
        
    Returns:
        str: HTML representation of the markdown text
    """
    # Convert markdown to HTML
    html = markdown.markdown(text)
    return html


def extract_structure(text: str) -> Dict[str, Any]:
    """
    Extract basic structure from text (headings, paragraphs, etc.)
    This can be used for more advanced formatting if needed.
    
    Args:
        text (str): Text to analyze
        
    Returns:
        Dict[str, Any]: Structure information
    """
    lines = text.split('\n')
    structure = {
        'headings': [],
        'paragraphs': [],
        'lists': []
    }
    
    current_paragraph = []
    in_list = False
    list_items = []
    
    for line in lines:
        line = line.strip()
        
        # Check for headings
        if line.startswith('#'):
            if current_paragraph:
                structure['paragraphs'].append(' '.join(current_paragraph))
                current_paragraph = []
            
            if in_list:
                structure['lists'].append(list_items)
                list_items = []
                in_list = False
                
            # Count the number of # to determine heading level
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break
                    
            heading_text = line[level:].strip()
            structure['headings'].append({
                'level': level,
                'text': heading_text
            })
        
        # Check for list items
        elif line.startswith('- ') or line.startswith('* ') or line.startswith('+ '):
            if current_paragraph:
                structure['paragraphs'].append(' '.join(current_paragraph))
                current_paragraph = []
                
            in_list = True
            list_items.append(line[2:].strip())
        
        # Empty line marks the end of a paragraph or list
        elif not line:
            if current_paragraph:
                structure['paragraphs'].append(' '.join(current_paragraph))
                current_paragraph = []
                
            if in_list:
                structure['lists'].append(list_items)
                list_items = []
                in_list = False
        
        # Regular text line
        else:
            if in_list:
                structure['lists'].append(list_items)
                list_items = []
                in_list = False
                
            current_paragraph.append(line)
    
    # Add any remaining content
    if current_paragraph:
        structure['paragraphs'].append(' '.join(current_paragraph))
        
    if in_list:
        structure['lists'].append(list_items)
    
    return structure


def process_text(text: str) -> str:
    """
    Process plain text for PDF generation.
    
    Args:
        text (str): Plain text to process
        
    Returns:
        str: Processed text
    """
    # For plain text, just return it cleaned
    return text.strip() 