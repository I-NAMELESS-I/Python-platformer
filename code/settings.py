import arcade

SCREEN_TITLE = 'Time Control Platformer'

# Пока None
PLAYER_SPEED = None
COOLDOWN_DURATION = None

KEYBINDS = {
    "move_left": arcade.key.A,
    "move_right": arcade.key.D,
    "jump": [arcade.key.W, arcade.key.SPACE],
    "fast_fall": arcade.key.S,
    "time_stop": arcade.key.T,
    "rewind": arcade.key.R,
    "select_object": arcade.MOUSE_BUTTON_LEFT
}