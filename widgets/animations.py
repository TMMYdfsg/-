# widgets/animations.py
from __future__ import annotations
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation
from kivy.metrics import dp


class ReceiptOverlay(ModalView):
    auto_dismiss = True

    def __init__(self, lines: list[str], **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        root = FloatLayout()
        with root.canvas.before:
            Color(0, 0, 0, 0.3)
            self.bg = RoundedRectangle(pos=(0, 0), size=(0, 0))
        self.add_widget(root)

        self.paper = FloatLayout(size_hint=(None, None), size=(dp(320), dp(460)))
        with self.paper.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = RoundedRectangle(
                pos=(0, 0), size=self.paper.size, radius=[(10, 10, 10, 10)]
            )
        self.lbl = Label(
            text="\n".join(lines),
            color=(0, 0, 0, 1),
            halign="left",
            valign="top",
            text_size=(self.paper.width - dp(24), None),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        self.paper.add_widget(self.lbl)
        root.add_widget(self.paper)
        self.root = root
        self.bind(on_open=self._animate_in)
        self.bind(size=self._on_resize)

    def _on_resize(self, *_):
        if hasattr(self, "bg"):
            self.bg.size = self.size

    def _animate_in(self, *_):
        w, h = self.size
        self.paper.pos = (w / 2 - self.paper.width / 2, h)
        anim = (
            Animation(y=h / 2 - self.paper.height / 2, d=0.45, t="out_cubic")
            + Animation(d=1.0)
            + Animation(y=-self.paper.height, d=0.35, t="in_cubic")
        )
        anim.bind(on_complete=lambda *_: self.dismiss())
        anim.start(self.paper)


class StampCardOverlay(ModalView):
    auto_dismiss = True

    def __init__(self, stamps: int, total: int = 10, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (1, 1)
        root = FloatLayout()
        with root.canvas.before:
            Color(0, 0, 0, 0.2)
            self.bg = RoundedRectangle(pos=(0, 0), size=(0, 0))
        self.add_widget(root)

        self.lbl = Label(
            text=f"スタンプ {stamps}/{total}",
            font_size="32sp",
            color=(1, 1, 1, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
        )
        root.add_widget(self.lbl)

        self.badge = Label(
            text="★",
            font_size="60sp",
            color=(1, 1, 0, 1),
            opacity=0,
            pos_hint={"center_x": 0.5, "center_y": 0.42},
        )
        root.add_widget(self.badge)

        self.bind(on_open=lambda *_: self._animate(stamps, total))
        self.bind(size=self._on_resize)

    def _on_resize(self, *_):
        if hasattr(self, "bg"):
            self.bg.size = self.size

    def _animate(self, stamps, total):
        if stamps in (total - 1, total):
            a = Animation(
                opacity=1, font_size="110sp", d=0.22, t="out_back"
            ) + Animation(font_size="60sp", d=0.25)
            a.start(self.badge)
