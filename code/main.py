import arcade
from code.core.menu_view import MenuView
from code.core.app_config import AppConfig, apply_window_config
from code.settings import SCREEN_TITLE

def main():
    try:
        from arcade.texture import Texture, TextureFilter  # type: ignore
        Texture.default_filter = TextureFilter.NEAREST
    except Exception:
        pass

    cfg = AppConfig.load()
    window = arcade.Window(width=cfg.width, height=cfg.height, title=SCREEN_TITLE, fullscreen=False)
    apply_window_config(window, cfg)

    menu_view = MenuView()
    window.show_view(menu_view)

    arcade.run()

if __name__ == "__main__":
    main()
