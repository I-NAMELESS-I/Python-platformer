import arcade

from code.entities.player import Player
# from code.entities.rewindable_object import RewindableObject
# from code.entities.static_platform import StaticPlatform
# from code.entities.moving_platform import MovingPlatform
#
# from code.time_system.time_system import TimeSystem
from code.core.input_manager import InputManager

class GameView(arcade.View, Player):
    def __init__(self):
        super().__init__()

        # Игрок
        self.player = Player(100, 100)

        # Список объектов, которые можно перематывать
        self.rewindable_objects = [] # логика 
        self.rewindable_objects_sprites = arcade.SpriteList() # спрайты

        # Статичные платформы 
        self.static_platforms = arcade.SpriteList()

        # Двигающиеся платформы, которые нелзя перематывать
        self.moving_platforms = [] # логика 
        self.moving_platform_sprites = arcade.SpriteList() # спрайты

        # Система времени
        self.time_system = None 

        # Input
        self.input_manager = InputManager(self.player, self.time_system, self.rewindable_objects)

        # Шипы
        self.death_zones = arcade.tilemap.process_layer(my_map, "DeathZones", use_spatial_hash=True)

        # Физика 
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=self.static_platforms + self.moving_platform_sprites + self.rewindable_objects_sprites,
            gravity_constant=1.0
        )

    # ОТРИСОВКА
    def on_draw(self):
        arcade.start_render()

        # Рисуем игрока
        self.player.draw()

        # Рисуем объекты
        for obj in self.static_platforms:
            obj.draw()
        for obj in self.moving_platform_sprites:
            obj.draw()
        for obj in self.rewindable_objects_sprites:
            obj.draw()

        # Рисуем UI 
        self.time_system.draw_ui()

    # ОБНОВЛЕНИЕ ЛОГИКИ
    def on_update(self, delta_time):
        self.input_manager.update(delta_time)
        self.physics_engine.update()

        # Обновляем игрока
        self.player.update_on_ground_state(self.physics_engine)
        self.player.update_animation(delta_time)

        # Обновляем систему времени
        self.time_system.update(delta_time, self.rewindable_objects)

        # Проверка на шипы
        if arcade.check_for_collision_with_list(self.player, self.death_zones):
            self.player.kill()

        # Логика движущихся платформ 
        for platform in self.moving_platforms:
            platform.update(delta_time) 
        
        # Логика выделяемых объектов 
        for obj in self.rewindable_objects:
            obj.update(delta_time)

    # INPUT
    def on_key_press(self, key, modifiers):
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        # Преобразуем координаты мыши в координаты мира
        world_x, world_y = self.camera.mouse_coordinates
        self.input_manager.on_mouse_press(world_x, world_y, button, modifiers)
