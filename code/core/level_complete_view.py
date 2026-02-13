import arcade
from code.core.game_over_view import GameOverView

class LevelCompleteView(GameOverView):
    def on_draw(self):
        self._ensure_layout()

        # Рисуем замороженный кадр игры
        self.game_view.on_draw()

        width, height = self.window.get_size()
        arcade.draw_lrbt_rectangle_filled(0, width, 0, height, (0, 0, 0, 180))

        arcade.draw_text(
            "УРОВЕНЬ ПРОЙДЕН!",
            width / 2,
            height * 0.65,
            arcade.color.WHITE,
            font_size=42,
            anchor_x="center",
        )

        self.ui.draw()
