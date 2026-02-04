from __future__ import annotations

from pathlib import Path

import arcade

from code.core.app_config import AppConfig
from code.core.game_view import GameView
from code.core.ui_widgets import Button, ButtonGroup
from code.settings import MAPS_DIR, SCREEN_TITLE


class LevelSelectView(arcade.View):
    """
    Экран выбора уровня списком.
    - ЛКМ по уровню: старт
    - Назад: кнопка или ESC
    """

    def __init__(self, back_view: arcade.View | None = None):
        super().__init__()
        self.back_view = back_view
        self.level_paths: list[Path] = sorted(MAPS_DIR.glob("*.tmx"))
        if not self.level_paths:
            self.level_paths.append(MAPS_DIR / "test_map.tmx")

        self.ui = ButtonGroup()
        self._layout_dirty = True

    def _ensure_layout(self):
        if not self._layout_dirty:
            return
        self._layout_dirty = False

        self.ui = ButtonGroup()
        width, height = self.window.get_size()

        button_w = min(560, width * 0.75)
        button_h = 44
        gap = 10
        top_y = height * 0.62

        # Кнопки уровней
        for i, path in enumerate(self.level_paths[:10]):  # чтобы не улететь за экран
            y = top_y - i * (button_h + gap)

            def make_start(p: Path):
                def _start():
                    cfg = AppConfig.load()
                    cfg.last_level = str(p)
                    cfg.save()
                    self.window.show_view(GameView(p))

                return _start

            self.ui.add(Button(path.stem, width / 2, y, button_w, button_h, make_start(path)))

        # Назад
        def back():
            self.go_back()

        self.ui.add(Button("Назад", width / 2, height * 0.18, min(320, width * 0.4), 52, back))

    def go_back(self):
        if self.back_view is not None:
            self.window.show_view(self.back_view)
        else:
            from code.core.menu_view import MenuView

            self.window.show_view(MenuView())

    def on_draw(self):
        self._ensure_layout()
        self.clear()
        width, height = self.window.get_size()

        arcade.draw_text(
            SCREEN_TITLE,
            width / 2,
            height * 0.80,
            arcade.color.WHITE,
            font_size=28,
            anchor_x="center",
        )
        arcade.draw_text(
            "ВЫБОР УРОВНЯ",
            width / 2,
            height * 0.72,
            arcade.color.LIGHT_GRAY,
            font_size=20,
            anchor_x="center",
        )

        if len(self.level_paths) > 10:
            arcade.draw_text(
                f"Показано 10 из {len(self.level_paths)} уровней",
                width / 2,
                height * 0.68,
                arcade.color.GRAY,
                font_size=12,
                anchor_x="center",
            )

        self.ui.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.go_back()

    def on_mouse_motion(self, x, y, dx, dy):
        self._ensure_layout()
        self.ui.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self._ensure_layout()
        self.ui.on_mouse_press(x, y, button)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._layout_dirty = True

