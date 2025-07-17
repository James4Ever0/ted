from textual.app import App, ComposeResult

from textual.widgets import TextArea, Button, Header, Footer, Static, Input
from textual.binding import Binding
from textual.screen import ModalScreen
from textual import events
import os
from typing import Optional
from pathlib import PurePath
from textual.widgets.text_area import BUILTIN_LANGUAGES
from textual.containers import Horizontal, Vertical

# TODO: command palette ctrl+p
# TODO: ctrl+f search
# TODO: ctrl+r replace
# TODO: ctrl+a select all
# TODO: ctrl+u undo shift+ctrl+u redo

# Constants for search direction
FIND_NEXT = 1
FIND_PREV = -1


class CodeEditor(TextArea):
    """Custom TextArea with enhanced indentation handling"""

    def key(self, event: events.Key) -> None:
        # Handle Tab with selection
        if event.key == "tab" and self.selection:
            selection = self.selection

            start_line = selection.start[0]
            end_line = selection.end[0]

            # Adjust end line if selection ends at column 0
            if selection.end[1] == 0 and end_line > start_line:
                end_line -= 1

            # Process selected lines
            if start_line <= end_line:
                with self.batch_update():
                    for line_no in range(start_line, end_line + 1):
                        self.insert_at((line_no, 0), self._get_indent_str())
                return

        # Handle Shift+Tab with selection
        elif event.key == "shift+tab" and self.selection:
            selection = self.selection
            start_line = selection.start[0]
            end_line = selection.end[0]

            # Adjust end line if selection ends at column 0
            if selection.end[1] == 0 and end_line > start_line:
                end_line -= 1

            # Process selected lines
            if start_line <= end_line:
                with self.batch_update():
                    for line_no in range(start_line, end_line + 1):
                        self._remove_indentation(line_no)
                return

        # Default behavior for other cases
        return super().key(event)

    def _get_indent_str(self) -> str:
        """Get appropriate indentation string based on settings"""
        return " " * self.indent_width if self.tab_behavior == "indent" else "\t"

    def _remove_indentation(self, line_no: int) -> None:
        """Remove one level of indentation from specified line"""
        line = self.document.get_line(line_no)
        if not line:
            return

        # Determine removal count based on tab behavior
        if self.tab_behavior == "indent":
            # Remove spaces up to indent_width
            count = 0
            for char in line:
                if char == " " and count < self.indent_width:
                    count += 1
                else:
                    break
            if count > 0:
                self.delete_range((line_no, 0), (line_no, count))
        else:
            # Remove single tab if present
            if line.startswith("\t"):
                self.delete_range((line_no, 0), (line_no, 1))


class SearchReplaceScreen(ModalScreen):
    """Modal screen for search/replace functionality"""

    BINDINGS = [Binding("escape", "dismiss", "Close")]

    def __init__(self, editor: TextArea, replace_mode: bool = False) -> None:
        super().__init__()
        self.editor = editor
        self.replace_mode = replace_mode
        self.last_search = ("", FIND_NEXT)

    def compose(self) -> ComposeResult:
        with Vertical(id="search-container"):
            yield Static("Find:" if not self.replace_mode else "Find and Replace")
            with Horizontal():
                yield Input(placeholder="Search term", id="search-term")
                if self.replace_mode:
                    yield Input(placeholder="Replace with", id="replace-term")

            with Horizontal(id="button-row"):
                yield Button("Next [Enter]", id="next")
                yield Button("Prev [Shift+Enter]", id="prev")
                if self.replace_mode:
                    yield Button("Replace", id="replace")
                    yield Button("Replace All", id="replace-all")
                yield Button("Close [Esc]", id="close")

    def on_mount(self) -> None:
        self.query_one("#search-term", Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search-term":
            self.find_next()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "next":
            self.find_next()
        elif event.button.id == "prev":
            self.find_prev()
        elif event.button.id == "replace":
            self.replace()
        elif event.button.id == "replace-all":
            self.replace_all()
        elif event.button.id == "close":
            self.dismiss()

    def find_next(self) -> None:
        self._find(FIND_NEXT)

    def find_prev(self) -> None:
        self._find(FIND_PREV)

    def _find(self, direction: int) -> None:
        search_term = self.query_one("#search-term", Input).value
        if not search_term:
            return

        self.last_search = (search_term, direction)
        found = self.editor.find_next(search_term, direction == FIND_PREV)
        if not found:
            self.app.notify("Text not found", severity="warning")

    def replace(self) -> None:
        search_term = self.query_one("#search-term", Input).value
        replace_term = self.query_one("#replace-term", Input).value

        if self.editor.selected_text == search_term:
            self.editor.replace(replace_term)
        self.find_next()

    def replace_all(self) -> None:
        search_term = self.query_one("#search-term", Input).value
        replace_term = self.query_one("#replace-term", Input).value
        self.editor.replace_all(search_term, replace_term)

    def action_dismiss(self) -> None:
        self.dismiss()


# TODO: use microsoft edit on supported platform (linux, windows)
class YesNoScreen(ModalScreen[str]):
    CSS_PATH = "editor.css"

    def compose(self) -> ComposeResult:
        self.buttons = [
            Button(compact=True, label="Save", id="save"),
            Button(compact=True, label="Quit", id="quit"),
            Button(compact=True, label="Resume", id="resume"),
        ]
        yield Static("Save before exit?")
        for it in self.buttons:
            yield it

    def on_button_pressed(self, event: Button.Pressed) -> None:
        ret = event.button.id
        self.dismiss(ret)

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            # close textual modal on escape key press
            self.dismiss("resume")
        elif event.key == "up":
            self.focus_previous("Button")
        elif event.key == "down":
            self.focus_next("Button")
        elif event.key == "left":
            self.focus_previous("Button")
        elif event.key == "right":
            self.focus_next("Button")


# since textual-editor is most likely bloatware, we don't want to adopt it but rip it apart.
def infer_language_from_filepath(file_path: str):
    file_extension = PurePath(file_path).suffix
    languages = {"." + e: e for e in BUILTIN_LANGUAGES}
    extensions = {
        ".yml": "yaml",
        ".py": "python",
        ".js": "javascript",
        ".md": "markdown",
        ".sh": "bash",
        ".rs": "rust",
    }
    if file_extension in languages:
        return languages[file_extension]
    if file_extension in extensions:
        return extensions[file_extension]


class TextEditorApp(App):
    """Textual-based text editor interface"""

    BINDINGS = [
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+r", "wrap", "Wrap"),
        # Binding("shift+ctrl+f", "search", "Find"),
        # Binding("shift+ctrl+r", "replace", "Replace"),
        # Binding("shift+ctrl+a", "select_all", "Select All"),
        # Binding("ctrl+shift+u", "undo", "Undo"),
        # Binding("ctrl+shift+r", "redo", "Redo"),
    ]
    CSS_PATH = "editor.css"  # or we can comment this out

    def __init__(
        self,
        filepath: Optional[str] = None,
        content: str = "",
        modified=False,
        language: Optional[str] = None,
        title: str = "ted",
        show_command_palette=False,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        assert content is not None
        self._title = title
        self.show_command_palette=show_command_palette
        self.filepath = filepath
        if language:
            self.language = language
        elif filepath:
            self.language = infer_language_from_filepath(filepath)
        else:
            self.language = None
        if self.language:
            assert self.language in BUILTIN_LANGUAGES
        self.initial_content = content
        self.result = content
        self.modified = modified
        self.saved = False
        self.text_area = TextArea.code_editor(
            text=self.initial_content,
            id="editor",
            language=self.language,
            soft_wrap=True,
            theme="vscode_dark",
            tab_behavior="indent",  # or "tab" for literal tabs
            # indent_width=4,
            # use_system_clipboard=True,
        )

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.text_area
        yield Footer(show_command_palette=self.show_command_palette)

    def on_mount(self) -> None:
        self.query_one(TextArea).focus()
        self.update_title()

    def update_title(self) -> None:
        title = self._title
        if self.filepath:
            title = f"{os.path.basename(self.filepath)} - {title}"
            if self.modified:
                title = f"*{title}"
        self.title = title

    def on_text_area_changed(self) -> None:
        self.modified = True
        self.saved = False
        self.update_title()

    def action_save(self) -> None:
        self.save_file()

    def action_quit(self) -> None:
        self.exit()

    def action_wrap(self) -> None:
        widget = self.query_one(TextArea)
        wrap_style = widget.soft_wrap
        widget.soft_wrap = not wrap_style

    def action_search(self) -> None:
        self.push_screen(SearchReplaceScreen(self.text_area))

    def action_replace(self) -> None:
        self.push_screen(SearchReplaceScreen(self.text_area, True))

    def action_select_all(self) -> None:
        self.text_area.select_all()

    def action_undo(self) -> None:
        self.text_area.undo()

    def action_redo(self) -> None:
        self.text_area.redo()

    def save_file(self) -> None:
        content = self.query_one(TextArea).text
        if self.filepath:
            try:
                with open(self.filepath, "w") as f:
                    f.write(content)
                self.modified = False
                self.saved = True
                self.update_title()
                self.notify(f"Saved to {self.filepath}")
            except OSError as e:
                self.notify(f"Save failed: {str(e)}", severity="error")
        self.result = content

    def prompt_for_saving(self):
        def _callback(msg: str):
            setattr(self, "exit_msg", msg)
            if msg == "save":
                self.save_file()
            if msg != "resume":
                self.super_exit()

        self.push_screen(YesNoScreen(), callback=_callback)

    def super_exit(self):
        super().exit()

    def exit(self) -> None:
        setattr(self, "exit_msg", "undefined")
        prompted = False
        if self.filepath:
            # prompt before save
            if self.modified:
                prompted = True
                self.prompt_for_saving()
        if not prompted:
            super().exit()
