import arcade
from code.core.game_view import GameView
from code.settings import SCREEN_TITLE

def main():
    # Размер монитора
    screen_width, screen_height = arcade.get_display_size()

    window = arcade.Window(
        width=screen_width,
        height=screen_height,
        title=SCREEN_TITLE,
        fullscreen=True
    )

    game_view = GameView()
    window.show_view(game_view)

    arcade.run()

if __name__ == "__main__":
    main()
