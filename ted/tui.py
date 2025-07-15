from textual.app import App, ComposeResult
from textual.widgets import Static, TextArea, Button, Footer, Header
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events, on
import os
from typing import Optional
from pathlib import PurePath
from textual.widgets.text_area import BUILTIN_LANGUAGES


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
            ...
        elif event.key == "down":
            ...
        elif event.key == "left":
            ...
        elif event.key == "right":
            ...


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
    }
    if file_extension in languages:
        return languages[file_extension]
    if file_extension in extensions:
        return extensions[file_extension]


class TextEditorApp(App):
    """Textual-based text editor interface"""

    BINDINGS = [
        Binding(key=key, action=action, description=action.title())
        for key, action in [
            ("ctrl+s", "save"),
            ("ctrl+q", "quit"),
            ("ctrl+r", "wrap"),
        ]
    ]
    CSS_PATH = "editor.css"  # or we can comment this out

    def __init__(
        self,
        filepath: Optional[str] = None,
        content: str = "",
        modified=False,
        language: Optional[str] = None,
        title: str = "ted",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        assert content is not None
        self._title = title
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

    def compose(self) -> ComposeResult:
        yield Header()
        yield TextArea.code_editor(
            self.initial_content, id="editor", language=self.language, soft_wrap=True
        )
        yield Footer(show_command_palette=False)

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
        self.update_title()

    def action_save(self) -> None:
        self.save_file()

    def action_quit(self) -> None:
        self.exit()

    def action_wrap(self) -> None:
        widget = self.query_one(TextArea)
        wrap_style = widget.soft_wrap
        widget.soft_wrap = not wrap_style

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
