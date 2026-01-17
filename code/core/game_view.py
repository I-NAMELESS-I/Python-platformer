import arcade
from code.entities.player import Player
from code.entities.rewindable_object import RewindableObject
from code.entities.static_platform import StaticPlatform
from code.entities.moving_platform import MovingPlatform
from code.time_system import TimeSystem

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Игрок
        self.player = Player(100, 100)

        # Список объектов, которые можно перематывать
        self.rewindable_objects = []

        # Статичные платформы 
        self.static_platforms = []

        # Двигающиеся платформы, которые нелзя перематывать
        self.moving_platforms = []

        # Система времени
        self.time_system = TimeSystem()

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

        # Обновляем систему времени
        self.time_system.update(delta_time, self.rewindable_objects)

    # ОБРАБОТКА КЛАВИШ
    def on_key_press(self, key, modifiers):
        # Передаём управление системе времени
        self.time_system.handle_key_press(key)

    # ОБРАБОТКА МЫШИ
    def on_mouse_press(self, x, y, button, modifiers):
        # Выбор объекта мышкой
        self.time_system.select_object_at(x, y, self.rewindable_objects)