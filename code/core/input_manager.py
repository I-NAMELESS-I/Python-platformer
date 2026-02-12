import arcade
from code.settings import KEYBINDS


class InputManager:
    def __init__(self, player, rewindable_objects=None):
        self.player = player
        self.rewindable_objects = rewindable_objects

        self.keybinds = KEYBINDS.copy()

        # Состояние клавиш
        self.keys = {
            "left": False,
            "right": False,
            "jump": False,
            "fast_fall": False,
        }

    # Вспомогательная функция для того, чтобы определить нажата ли та кнопка
    def check(self, action, key) -> bool:
        bind = self.keybinds[action]
        if isinstance(bind, list):
            return key in bind
        return key == bind

    # KEY PRESS
    def on_key_press(self, key, modifiers):

        if self.check("move_left", key):
            self.keys["left"] = True

        if self.check("move_right", key):
            self.keys["right"] = True

        if self.check("jump", key):
            self.keys["jump"] = True

        if self.check("fast_fall", key):
            self.keys["fast_fall"] = True

        if self.check("time_stop", key):
            for pl in self.rewindable_objects:
                pl.start_pause()

        if self.check("rewind", key):
            for pl in self.rewindable_objects:
                pl.start_rewind()

    # KEY RELEASE
    def on_key_release(self, key, modifiers):

        if self.check("move_left", key):
            self.keys["left"] = False

        if self.check("move_right", key):
            self.keys["right"] = False

        if self.check("jump", key):
            self.keys["jump"] = False

        if self.check("fast_fall", key):
            self.keys["fast_fall"] = False

        if self.check("time_stop", key):
            for pl in self.rewindable_objects:
                pl.stop_pause()

        if self.check("rewind", key):
            for pl in self.rewindable_objects:
                pl.stop_rewind()

    # MOUSE PRESS — выбор объекта
    def on_mouse_press(self, x, y, button, modifiers):
        pass

    # UPDATE
    def update(self, delta_time):

        if self.keys["left"] and not self.keys["right"]:
            self.player.move_left()

        elif self.keys["right"] and not self.keys["left"]:
            self.player.move_right()

        else:
            self.player.stop_horizontal()

        # Может совершаться только если игрок не на земле
        if self.keys["fast_fall"]:
            self.player.fast_fall()

        # Может совершаться только если игрок на земле
        if self.keys["jump"]:
            self.player.jump()         