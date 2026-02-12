from pathlib import Path

import arcade

from code.core.game_view import GameView
from code.core.level_select_view import LevelSelectView
from code.core.app_config import AppConfig
from code.core.settings_view import SettingsView
from code.core.rules_view import RulesView
from code.core.ui_widgets import Button, ButtonGroup
from code.settings import MAPS_DIR, SCREEN_TITLE


class MenuView(arcade.View):
    """
    Главное меню:
      - Играть: запускает последний открытый уровень
      - Выбор уровня: открывает список уровней
      - Настройки
      - Выход
    """

    def __init__(self):
        super().__init__()
        self.level_paths: list[Path] = sorted(MAPS_DIR.glob("*.tmx"))
        self.ui = ButtonGroup()
        self._layout_dirty = True

        if not self.level_paths:
            self.level_paths.append(MAPS_DIR / "test_map.tmx")

    def _ensure_layout(self):
        if not self._layout_dirty:
            return
        self._layout_dirty = False

        self.ui = ButtonGroup()
        width, height = self.window.get_size()
        button_w = min(380, width * 0.45)
        button_h = 52
        gap = 12
        base_y = height * 0.22

        def start_last():
            self.start_last_level()

        def level_select():
            self.window.show_view(LevelSelectView(back_view=self))

        def open_settings():
            self.window.show_view(SettingsView(back_view=self))

        def open_rules():
            self.window.show_view(RulesView(back_view=self))

        def quit_game():
            arcade.exit()

        self.ui.add(Button("Играть", width / 2, base_y + (button_h + gap) * 4, button_w, button_h, start_last))
        self.ui.add(Button("Выбор уровня", width / 2, base_y + (button_h + gap) * 3, button_w, button_h, level_select))
        self.ui.add(Button("Правила", width / 2, base_y + (button_h + gap) * 2, button_w, button_h, open_rules))
        self.ui.add(Button("Настройки", width / 2, base_y + (button_h + gap) * 1, button_w, button_h, open_settings))
        self.ui.add(Button("Выход", width / 2, base_y + (button_h + gap) * 0, button_w, button_h, quit_game))


    def on_draw(self):
        self._ensure_layout()
        self.clear()
        width, height = self.window.get_size()

        title = SCREEN_TITLE
        arcade.draw_text(
            title,
            width / 2,
            height * 0.75,
            arcade.color.WHITE,
            font_size=32,
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
        self.ui.on_mouse_press(x, y, button)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._layout_dirty = True

    def start_last_level(self):
        cfg = AppConfig.load()
        last = Path(cfg.last_level) if cfg.last_level else None
        if last and last.exists():
            level_path = last
        else:
            level_path = self.level_paths[0]

        cfg.last_level = str(level_path)
        cfg.save()
        self.window.show_view(GameView(level_path))
