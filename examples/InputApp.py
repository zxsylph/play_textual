
from typing import List, Optional, Tuple, Union

import rich.box
from rich.panel import Panel
from rich.style import Style

from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual import events


class Input(Widget):
    
    _has_focus: Reactive[bool] = Reactive(False)
    value: Reactive[str] = Reactive("")

    def __init__(self, *,
        name: Optional[str] = None,
        value: str = "",
        placeholder: str = "",
        title: str = "",) -> None:
        super().__init__()
        self.name = name
        self._has_focus: False
        self.value = value
        self.placeholder = placeholder
        self.title = title


    def render(self) -> Panel:
        if (
            self.title
            and not self.placeholder
            and len(self.value) == 0
            and not self.has_focus
        ):
            title = ""
        else:
            title = self.title

        text = self.value

        return Panel(
            text,
            title=title,
            title_align="left",
            height=3,
            style=self.style or "",
            border_style=self.border_style or Style(color="blue"),
            box=rich.box.DOUBLE if self.has_focus else rich.box.SQUARE,
        )

    @property
    def has_focus(self) -> bool:
        """Produces True if widget is focused"""
        return self._has_focus

    async def on_focus(self, event: events.Focus) -> None:
        self._has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self._has_focus = False        

    async def on_key(self, event: events.Key) -> None:
        if len(event.key) == 1 and event.key.isprintable():
            self.value = self.value + event.key
        event.stop()


class InputApp(App):
    """Demonstrates custom widgets"""

    async def on_mount(self) -> None:
        await self.bind("q", "quit", "Quit")
        self.inputs = list(Input(name=f"Name {i}", value=i, title=f"Title {i}") for i in range(5))
        await self.view.dock(*self.inputs, edge="top")



InputApp.run(log="textual.log")