"""E Read Tool application entry point."""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Keep Kivy from writing logs outside the project on restricted Windows setups.
os.environ.setdefault("KIVY_NO_FILELOG", "1")

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget


BACKGROUND = (0.965, 0.957, 0.925, 1)
SURFACE = (1, 1, 1, 1)
PRIMARY = (0.20, 0.34, 0.27, 1)
PRIMARY_PRESSED = (0.15, 0.27, 0.21, 1)
TEXT = (0.14, 0.16, 0.15, 1)
MUTED_TEXT = (0.42, 0.45, 0.43, 1)


def find_chinese_font() -> str:
    """Use a Windows Chinese font for the desktop prototype when available."""
    if sys.platform == "win32":
        font_dir = Path(os.environ.get("WINDIR", r"C:\Windows")) / "Fonts"
        for filename in ("msyh.ttc", "simhei.ttf", "simsun.ttc"):
            candidate = font_dir / filename
            if candidate.exists():
                return str(candidate)
    return "Roboto"


FONT_NAME = find_chinese_font()


class RoundedPanel(BoxLayout):
    """A layout with a rounded solid background."""

    def __init__(self, background_color=SURFACE, radius=20, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._background_color = Color(*background_color)
            self._background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(radius)],
            )
        self.bind(pos=self._update_background, size=self._update_background)

    def _update_background(self, *_args) -> None:
        self._background.pos = self.pos
        self._background.size = self.size


class BookshelfView(BoxLayout):
    """The M1 bookshelf screen with an empty state."""

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            padding=[dp(24), dp(24), dp(24), dp(20)],
            spacing=dp(18),
            **kwargs,
        )

        with self.canvas.before:
            Color(*BACKGROUND)
            self._background = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_background, size=self._update_background)

        header = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(12))
        title = Label(
            text="我的书架",
            font_name=FONT_NAME,
            font_size=sp(25),
            bold=True,
            color=TEXT,
            halign="left",
            valign="middle",
        )
        title.bind(size=lambda label, _size: setattr(label, "text_size", label.size))

        import_button = Button(
            text="导入 TXT",
            font_name=FONT_NAME,
            font_size=sp(15),
            bold=True,
            size_hint=(None, None),
            size=(dp(112), dp(44)),
            background_normal="",
            background_down="",
            background_color=PRIMARY,
            color=(1, 1, 1, 1),
        )
        import_button.bind(state=self._update_button_color)
        import_button.bind(on_release=self._show_m2_message)

        header.add_widget(title)
        header.add_widget(import_button)
        self.add_widget(header)

        self.add_widget(Widget(size_hint_y=0.18))

        empty_panel = RoundedPanel(
            orientation="vertical",
            padding=[dp(24), dp(34)],
            spacing=dp(12),
            size_hint_y=None,
            height=dp(230),
        )
        empty_panel.add_widget(
            Label(
                text="暂无书籍",
                font_name=FONT_NAME,
                font_size=sp(22),
                bold=True,
                color=TEXT,
            )
        )
        self.empty_message = Label(
            text="书架还是空的\n导入一本 TXT 开始阅读",
            font_name=FONT_NAME,
            font_size=sp(16),
            color=MUTED_TEXT,
            halign="center",
            valign="middle",
            line_height=1.45,
        )
        self.empty_message.bind(
            size=lambda label, _size: setattr(label, "text_size", label.size)
        )
        empty_panel.add_widget(self.empty_message)
        self.add_widget(empty_panel)

        self.add_widget(Widget(size_hint_y=0.45))
        self.add_widget(
            Label(
                text="E Read Tool · 本地 TXT 阅读器",
                font_name=FONT_NAME,
                font_size=sp(12),
                color=MUTED_TEXT,
                size_hint_y=None,
                height=dp(24),
            )
        )

    def _update_background(self, *_args) -> None:
        self._background.pos = self.pos
        self._background.size = self.size

    @staticmethod
    def _update_button_color(button: Button, state: str) -> None:
        button.background_color = PRIMARY_PRESSED if state == "down" else PRIMARY

    def _show_m2_message(self, _button: Button) -> None:
        self.empty_message.text = "导入功能将在 M2 实现\n当前已完成书架空状态"


class EReadToolApp(App):
    title = "E Read Tool"

    def build(self) -> BookshelfView:
        Window.clearcolor = BACKGROUND
        Window.size = (420, 760)
        return BookshelfView()


if __name__ == "__main__":
    EReadToolApp().run()
