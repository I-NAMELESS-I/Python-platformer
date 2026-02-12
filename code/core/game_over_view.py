import arcade

from code.core.ui_widgets import Button, ButtonGroup


class GameOverView(arcade.View):

    def __init__(self, game_view: arcade.View):
        super().__init__()
        self.game_view = game_view
        self.ui = ButtonGroup()
        self._layout_dirty = True

    def _ensure_layout(self):
        if not self._layout_dirty:
            return
        self._layout_dirty = False

        self.ui = ButtonGroup()
        width, height = self.window.get_size()

        button_w = min(420, width * 0.5)
        button_h = 56
        gap = 14
        start_y = height * 0.55

        def restart():
            from code.core.game_view import GameView

            map_path = getattr(self.game_view, "map_path", None)
            self.window.show_view(GameView(map_path))

        def to_menu():
            from code.core.menu_view import MenuView

            self.window.show_view(MenuView())

        def quit_game():
            arcade.exit()

        self.ui.add(Button("Рестарт уровня", width / 2, start_y - (button_h + gap) * 1, button_w, button_h, restart))
        self.ui.add(Button("Меню", width / 2, start_y - (button_h + gap) * 2, button_w, button_h, to_menu))
        self.ui.add(Button("Выход", width / 2, start_y - (button_h + gap) * 3, button_w, button_h, quit_game))

    def on_draw(self):
        self._ensure_layout()

        # Сначала рисуем "замороженный" кадр игры
        self.game_view.on_draw()

        # Затем — затемнение и текст
        width, height = self.window.get_size()
        arcade.draw_lrbt_rectangle_filled(0, width, 0, height, (0, 0, 0, 180))

        arcade.draw_text(
            "GAME OVER!",
            width / 2,
            height * 0.65,
            arcade.color.WHITE,
            font_size=42,
            anchor_x="center",
        )

        self.ui.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        self._ensure_layout()
        self.ui.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self._ensure_layout()
        self.ui.on_mouse_press(x, y, button)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self._layout_dirty = True