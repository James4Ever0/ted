
<div align="center">

<!-- TODO: Add a screenshot -->
<!-- TODO: Make the text in ted logo partially selected, and put a cursor around the selected area, use monospace font for the text -->

<img src="https://raw.githubusercontent.com/james4ever0/ted/master/logo/ted-black.jpeg" alt="logo" width="270"/>

<p align="center">A simple TUI editor with a CLI and API using Textual</p>
<p align="center">
<a href="https://github.com/james4ever0/ted/blob/master/LICENSE"><img alt="License: WTFPL" src="https://img.shields.io/badge/license-UNLICENSE-green.svg?style=flat"></a>
<a href="https://pypi.org/project/ted-editor/"><img alt="PyPI" src="https://img.shields.io/pypi/v/ted-editor"></a>
<a href="https://deepwiki.com/James4Ever0/ted"><img src="https://deepwiki.com/badge.svg" alt="Ask DeepWiki"></a>
<a href="https://pepy.tech/projects/ted-editor"><img src="https://static.pepy.tech/badge/ted-editor" alt="PyPI Downloads"></a>
<a href="https://github.com/james4ever0/ted"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>
</div>

## Video demo

![ted_demo](https://github.com/user-attachments/assets/93b59739-40cd-4e07-bb32-0cfa5adfbec1)

## Installation
```bash
# without syntax highlight
pip install ted-editor

# with syntax highlight
pip install ted-editor[syntax]
```

### Key Features

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

### Usage

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

[edit](https://github.com/microsoft/edit) (Microsoft rewrite in Rust)

[textual-editor](https://github.com/kyrlian/textual-editor) (Most similar, with a directory tree tab)

[TED](https://texteditors.org/cgi-bin/wiki.pl?TED) (MS-DOS)

[ted](https://github.com/robdelacruz/ted) (Go implementation)
