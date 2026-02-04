from __future__ import annotations

import arcade

from code.core.app_config import AppConfig, apply_window_config
from code.core.ui_widgets import Button, ButtonGroup
from code.settings import SCREEN_TITLE


class SettingsView(arcade.View):
    """
    Настройки окна:
      - выбор разрешения
      - режим окно / fullscreen
    Управление мышью (кнопки), ESC — назад.
    """

    RESOLUTIONS: list[tuple[int, int]] = [
        (1280, 720),
        (1366, 768),
        (1600, 900),
        (1920, 1080),
    ]

    def __init__(self, back_view: arcade.View | None = None):
        super().__init__()
        self.back_view = back_view
        self.cfg = AppConfig.load()

        self.ui = ButtonGroup()
        self._layout_dirty = True

    def _resolution_index(self) -> int:
        try:
            return self.RESOLUTIONS.index((int(self.cfg.width), int(self.cfg.height)))
        except ValueError:
            return 0

    def _ensure_layout(self):
        if not self._layout_dirty:
            return
        self._layout_dirty = False

        self.ui = ButtonGroup()
        width, height = self.window.get_size()

        button_w = min(520, width * 0.6)
        button_h = 56
        gap = 14
        start_y = height * 0.55

        def toggle_fullscreen():
            self.cfg.fullscreen = not self.cfg.fullscreen
            # сразу применяем, чтобы было видно
            apply_window_config(self.window, self.cfg)
            self._layout_dirty = True

        def prev_res():
            idx = self._resolution_index()
            idx = (idx - 1) % len(self.RESOLUTIONS)
            self.cfg.width, self.cfg.height = self.RESOLUTIONS[idx]
            apply_window_config(self.window, self.cfg)
            self._layout_dirty = True

        def next_res():
            idx = self._resolution_index()
            idx = (idx + 1) % len(self.RESOLUTIONS)
            self.cfg.width, self.cfg.height = self.RESOLUTIONS[idx]
            apply_window_config(self.window, self.cfg)
            self._layout_dirty = True

        def save_and_back():
            self.cfg.save()
            self.go_back()

        def back_no_save():
            self.go_back()

        # Кнопки
        fs_label = "Режим: FULLSCREEN" if self.cfg.fullscreen else "Режим: ОКНО"
        res_label = f"Разрешение: {self.cfg.width}×{self.cfg.height}"

        self.ui.add(Button(fs_label, width / 2, start_y, button_w, button_h, toggle_fullscreen))
        self.ui.add(Button("Разрешение: <  " + res_label + "  >", width / 2, start_y - (button_h + gap) * 1, button_w, button_h, next_res))

        self.ui.add(Button("Сохранить и назад", width / 2, start_y - (button_h + gap) * 2.5, button_w, button_h, save_and_back))
        self.ui.add(Button("Назад (без сохранения)", width / 2, start_y - (button_h + gap) * 3.5, button_w, button_h, back_no_save))

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
            height * 0.78,
            arcade.color.WHITE,
            font_size=28,
            anchor_x="center",
        )
        arcade.draw_text(
            "НАСТРОЙКИ",
            width / 2,
            height * 0.70,
            arcade.color.LIGHT_GRAY,
            font_size=22,
            anchor_x="center",
        )

        self.ui.draw()

    def on_key_press(self, key, modifiers):
        return

    def on_mouse_motion(self, x, y, dx, dy):
        self._ensure_layout()
        self.ui.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self._ensure_layout()
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if len(self.ui.buttons) > 1 and self.ui.buttons[1].contains(x, y):
                idx = self._resolution_index()
                idx = (idx - 1) % len(self.RESOLUTIONS)
                self.cfg.width, self.cfg.height = self.RESOLUTIONS[idx]
                apply_window_config(self.window, self.cfg)
                self._layout_dirty = True
                return
        self.ui.on_mouse_press(x, y, button)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._layout_dirty = True

