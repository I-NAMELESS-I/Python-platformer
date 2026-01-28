import arcade
from pathlib import Path

# Базовая директория проекта (корень репозитория)
BASE_DIR = Path(__file__).resolve().parent.parent

# Директории ресурсов
ASSETS_DIR = BASE_DIR / "assets"
MAPS_DIR = ASSETS_DIR / "maps"
SPRITES_DIR = ASSETS_DIR / "sprites"

SCREEN_TITLE = "Time Control Platformer"

# Пока None
COOLDOWN_DURATION = None

KEYBINDS = {
    "move_left": arcade.key.A,
    "move_right": arcade.key.D,
    "jump": [arcade.key.W, arcade.key.SPACE],
    "fast_fall": arcade.key.S,
    "time_stop": arcade.key.T,
    "rewind": arcade.key.R,
    "select_object": arcade.MOUSE_BUTTON_LEFT,
}