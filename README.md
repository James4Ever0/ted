# ted - Terminal Text Editor

A simple TUI text editor using Textual.

## Installation
```bash
pip install ted-editor
```

## CLI Usage
```bash
ted [filepath]
```

## API Usage

```python
from ted import edit

content = edit(content="Initial text", filepath="demo.txt")
```

### Key Features:

1. **Dual Interface**:
   - CLI: `ted <filepath>`
   - API: `ted.edit(content, filepath)`

2. **File Handling**:
   - Prompt for file path if not provided
   - Ask for file creation if doesn't exist
   - Handle permission errors

3. **TUI Editor**:
   - Textual-based interface
   - Save with Ctrl+S or Save button
   - Quit with Ctrl+Q or Quit button
   - Shows modification status in title
   - Auto-save on quit if modified

4. **API Behavior**:
   - `content=None`: Load from file if exists
   - `filepath=None`: Memory-only editing
   - Returns edited content

### Usage Examples:

**CLI:**
```bash
ted  # Prompts for file path
ted myfile.txt
```

**API:**
```python
from ted import edit

# Edit existing file
content = edit(filepath="existing.txt")

# Create new file
new_content = edit(content="New content", filepath="new.txt")

# Memory-only editing
temp_content = edit(content="Temporary text")
```

## See also

[edit](https://github.com/microsoft/edit)

[textual-editor](https://github.com/kyrlian/textual-editor)