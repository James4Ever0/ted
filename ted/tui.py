from textual.app import App, ComposeResult
from textual.widgets import TextArea, Button, Footer, Header
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events, on
import os
from typing import Optional


# since textual-editor is most likely bloatware, we don't want to adopt it.
# TODO: enable word wrap, make word wrap as default, can be toggled with a keyboard shortcut switch ctrl+w

class TextEditorApp(App):
    """Textual-based text editor interface"""
    
    BINDINGS = [Binding(key=key, action=action, description=action.title()) for key, action in [
      ("ctrl+s", "save"), 
      ("ctrl+q", "quit"), 
      ("ctrl+r", "wrap"),
      ]]
    CSS_PATH = "editor.css" # or we can comment this out

    def __init__(self, filepath: Optional[str] = None, content: str= "", modified=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert content is not None
        self.filepath = filepath
        self.initial_content = content
        self.result = content
        self.modified = modified
        
    def compose(self) -> ComposeResult:
        yield Header()
        yield TextArea.code_editor(self.initial_content, id="editor")
        yield Footer(show_command_palette=False)
        
    def on_mount(self) -> None:
        self.query_one(TextArea).focus()
        self.update_title()
        
    def update_title(self) -> None:
        title = "ted"
        if self.filepath:
            title = f"{os.path.basename(self.filepath)} - {title}"
        if self.modified:
            title = f"*{title}"
        self.title = title
        
    def on_text_area_changed(self) -> None:
        self.modified = True
        self.update_title()
        
    def action_save(self) -> None:
        self.save_file()
        
    def action_quit(self) -> None:
        self.exit()
    
    def action_wrap(self) -> None:
        widget = self.query_one(TextArea)
        wrap_style = widget.styles.text_wrap
        if wrap_style == "nowrap":
            widget.styles.text_wrap = "wrap"
        else:
            widget.styles.text_wrap = "nowrap"
        
    def save_file(self) -> None:
        content = self.query_one(TextArea).text
        if self.filepath:
            try:
                with open(self.filepath, "w") as f:
                    f.write(content)
                self.modified = False
                self.update_title()
                self.notify(f"Saved to {self.filepath}")
            except OSError as e:
                self.notify(f"Save failed: {str(e)}", severity="error")
        self.result = content
        
    def key_ctrl_q(self) -> None:
        self.exit()
        
    def exit(self) -> None:
        if self.modified:
            # prompt before save
            ...
            # self.save_file()
        super().exit()