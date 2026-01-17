import arcade

from code.entities.player import Player
from code.entities.rewindable_object import RewindableObject
from code.entities.static_platform import StaticPlatform
from code.entities.moving_platform import MovingPlatform

from code.time_system import TimeSystem
from code.core.input_manager import InputManeger

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Игрок
        self.player = None

        # Список объектов, которые можно перематывать
        self.rewindable_objects = []

        # Статичные платформы 
        self.static_platforms = []

        # Двигающиеся платформы, которые нелзя перематывать
        self.moving_platforms = []

        # Система времени
        self.time_system = None 

        # Input
        self.input_manager = None

    # ОТРИСОВКА
    def on_draw(self):
        arcade.start_render()

        # Рисуем игрока
        self.player.draw()

        # Рисуем объекты
        for obj in self.rewindable_objects:
            obj.draw()

        for obj in self.moving_platforms:
            obj.draw()

        for obj in self.static_platforms:
            obj.draw()

        # Рисуем UI 
        self.time_system.draw_ui()

    # ОБНОВЛЕНИЕ ЛОГИКИ
    def on_update(self, delta_time):
        # Обновляем игрока
        self.player.update(delta_time)

        # Обновляем объекты
        for obj in self.rewindable_objects:
            obj.update(delta_time)

        for obj in self.moving_platforms:
            obj.update(delta_time)

        for obj in self.static_platforms:
            obj.update(delta_time)

        # Обновляем систему времени
        self.time_system.update(delta_time, self.rewindable_objects)

    # INPUT
    def on_key_press(self, key, modifiers):
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        # Преобразуем координаты мыши в координаты мира
        world_x, world_y = self.camera.mouse_coordinates
        self.input_manager.on_mouse_press(world_x, world_y, button, modifiers)
