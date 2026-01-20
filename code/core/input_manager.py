import arcade
from code.settings import KEYBINDS

class InputManager:
    def __init__(self, player, time_system, rewindable_objects):
        self.player = player
        self.time_system = time_system
        self.rewindable_objects = rewindable_objects

        self.keybinds = KEYBINDS.copy()

        # Состояние клавиш
        self.keys = {
            "left": False,
            "right": False,
            "jump": False,
            "fast_fall": False,
            "select_object": False
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
            self.time_system.toggle_time_stop()

        if self.check("rewind", key):
            self.time_system.start_rewind()

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

    # MOUSE PRESS — выбор объекта
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.check("select_object", button):
            return

        for obj in self.rewindable_objects:
            if obj.sprite and obj.sprite.collides_with_point((x, y)):
                self.time_system.select_object(obj)
                return

        # Очистка выбора объекта
        self.time_system.clear_selection()

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