import argparse
import os
import sys
from .tui import TextEditorApp

def validate_filepath(filepath: str) -> str:
    """Handle file path validation and user prompts."""
    if not filepath:
        filepath = input("Enter file path: ").strip()
        if not filepath:
            print("No file path provided. Exiting.")
            sys.exit(1)

    if os.path.exists(filepath):
        if not os.access(filepath, os.R_OK | os.W_OK):
            print(f"Error: Permission denied for '{filepath}'")
            sys.exit(1)
    else:
        create = input(f"File '{filepath}' doesn't exist. Create it? [y/N]: ").lower()
        if create != 'y':
            print("Aborted.")
            sys.exit(0)
            
        # Validate directory permissions
        dir_path = os.path.dirname(filepath) or "."
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        if not os.access(dir_path, os.W_OK):
            print(f"Error: Permission denied to create file in '{dir_path}'")
            sys.exit(1)
            
    return filepath

def main():
    parser = argparse.ArgumentParser(description='ted - Terminal Text Editor')
    parser.add_argument('filepath', nargs='?', help='File to edit')
    args = parser.parse_args()
    
    try:
        filepath = validate_filepath(args.filepath)
        TextEditorApp(filepath=filepath).run()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)