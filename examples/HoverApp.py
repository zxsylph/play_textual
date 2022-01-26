from rich.panel import Panel

from typing import Any, Callable, ClassVar, Type, TypeVar

from textual.app import App
from textual.reactive import Reactive
from textual.widget import Widget
from textual import events


class Hover(Widget):
    

    _has_focus: Reactive[bool] = Reactive(False)

    def __init__(self, log="textual.log") -> None:
        super().__init__()
        self.log_file = open(log, "wt") if log else None

    def log(self, *args: Any, verbosity: int = 1, **kwargs) -> None:
        """Write to logs.

        Args:
            *args (Any): Positional arguments are converted to string and written to logs.
            verbosity (int, optional): Verbosity level 0-3. Defaults to 1.
        """
        try:
            if self.log_file and verbosity <= self.log_verbosity:
                output = f" ".join(str(arg) for arg in args)
                if kwargs:
                    key_values = " ".join(
                        f"{key}={value}" for key, value in kwargs.items()
                    )
                    output = " ".join((output, key_values))
                self.log_file.write(output + "\n")
                self.log_file.flush()
        except Exception:
            pass

    mouse_over = Reactive(False)
    style = Reactive("on white")

    def render(self) -> Panel:
        # return Panel(self.style, style=("on red" if self.mouse_over else self.style))
        return Panel(self.style, style=self.style, border_style=("red" if self.mouse_over else 'none'))

    def on_enter(self) -> None:
        self.mouse_over = True
        self._has_focus = True

    def on_leave(self) -> None:
        self.mouse_over = False
        self._has_focus = False

    async def on_focus(self, event: events.Focus) -> None:
        self._has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self._has_focus = False        

    async def on_key(self, event: events.Key) -> None:
        self.log(event.key)
        if self._has_focus:
            if event.key.isdigit():
                self.style = f"on color({event.key})"


class HoverApp(App):
    """Demonstrates custom widgets"""

    async def on_mount(self) -> None:
        await self.bind("q", "quit", "Quit")
        self.hovers = list(Hover() for _ in range(5))
        # self.hovers = []
        # self.hovers.append(Hover())
        await self.view.dock(*self.hovers, edge="top")

    # async def on_key(self, event) -> None:
    #     for item in self.hovers:
    #         if item.has_focus:
    #             item.on_key(event)



HoverApp.run(log="textual.log")