from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

import arcade


@dataclass
class Button:
    text: str
    center_x: float
    center_y: float
    width: float
    height: float
    on_click: Callable[[], None]
    enabled: bool = True

    def contains(self, x: float, y: float) -> bool:
        half_w = self.width / 2
        half_h = self.height / 2
        return (
            self.center_x - half_w <= x <= self.center_x + half_w
            and self.center_y - half_h <= y <= self.center_y + half_h
        )

    def draw(self, hovered: bool = False):
        left = self.center_x - self.width / 2
        right = self.center_x + self.width / 2
        bottom = self.center_y - self.height / 2
        top = self.center_y + self.height / 2

        if not self.enabled:
            fill = (60, 60, 60, 180)
            border = (120, 120, 120, 220)
            text_color = arcade.color.GRAY
        else:
            fill = (40, 40, 40, 200) if not hovered else (70, 70, 70, 220)
            border = arcade.color.LIGHT_GRAY if not hovered else arcade.color.WHITE
            text_color = arcade.color.WHITE if hovered else arcade.color.LIGHT_GRAY

        if hasattr(arcade, "draw_rectangle_filled"):
            arcade.draw_rectangle_filled(self.center_x, self.center_y, self.width, self.height, fill)
        else:
            arcade.draw_lrbt_rectangle_filled(left, right, bottom, top, fill)

        if hasattr(arcade, "draw_rectangle_outline"):
            arcade.draw_rectangle_outline(self.center_x, self.center_y, self.width, self.height, border, border_width=2)
        else:
            if hasattr(arcade, "draw_lrbt_rectangle_outline"):
                try:
                    arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, border, border_width=2)
                except TypeError:
                    arcade.draw_lrbt_rectangle_outline(left, right, bottom, top, border, line_width=2)

        arcade.draw_text(
            self.text,
            self.center_x,
            self.center_y,
            text_color,
            font_size=18,
            anchor_x="center",
            anchor_y="center",
        )


class ButtonGroup:
    def __init__(self):
        self.buttons: list[Button] = []
        self._hover_index: Optional[int] = None

    def add(self, button: Button):
        self.buttons.append(button)

    def on_mouse_motion(self, x: float, y: float):
        self._hover_index = None
        for i, b in enumerate(self.buttons):
            if b.enabled and b.contains(x, y):
                self._hover_index = i
                break

    def on_mouse_press(self, x: float, y: float, button: int):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return
        for b in self.buttons:
            if b.enabled and b.contains(x, y):
                b.on_click()
                return

    def draw(self):
        for i, b in enumerate(self.buttons):
            b.draw(hovered=(i == self._hover_index))
