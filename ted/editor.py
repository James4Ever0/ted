import os
from .tui import TextEditorApp
from typing import Optional

def edit(content: Optional[str] = None, filepath: Optional[str] = None, return_format:str="content") -> str:
    """
    API interface for text editing
    
    Args:
        content: Initial content (optional)
        filepath: File to edit (optional)
        
    Returns:
        Edited content as string
    """
    # Handle file validation
    initial_content = content or ""
    if filepath and os.path.exists(filepath):
        if not os.access(filepath, os.R_OK | os.W_OK):
            raise PermissionError(f"Access denied for '{filepath}'")
        if content is None:
            with open(filepath, 'r') as f:
                initial_content = f.read()
    
    # Run editor and return content
    editor = TextEditorApp(filepath=filepath, content=initial_content)
    editor.run()
    
    if return_format == "content":
        return editor.result
    else:
        raise ValueError("Unknown return format:", return_format)