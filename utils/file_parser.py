"""
Utility functions for file parsing
"""
from pathlib import Path
from typing import Optional


def parse_text_file(file_path: str) -> str:
    """
    Read and parse a text file from the given file path
    
    Args:
        file_path: Path to the text file
        
    Returns:
        str: Content of the file
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not a text file
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {file_path}")
    
    # Check if it's a text file
    if path.suffix not in ['.txt', '.md', '.text']:
        raise ValueError(f"File must be a text file (.txt, .md, .text): {file_path}")
    
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return content


def validate_text_content(text: str, min_words: int = 50) -> tuple[bool, Optional[str]]:
    """
    Validate that text content has sufficient information
    
    Args:
        text: Text content to validate
        min_words: Minimum number of words required
        
    Returns:
        tuple: (is_valid: bool, error_message: Optional[str])
    """
    if not text or not text.strip():
        return False, "Text content is empty"
    
    word_count = len(text.split())
    if word_count < min_words:
        return False, f"Text content too short ({word_count} words, minimum {min_words} required)"
    
    return True, None
