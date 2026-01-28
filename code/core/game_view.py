import arcade

from code.entities.player import Player
from code.core.input_manager import InputManager
from code.settings import MAPS_DIR


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Камера для мира и для UI
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.camera.zoom = 2

        # Загружаем карту уровня
        map_path = MAPS_DIR / "test_map.tmx"
        self.tile_map = arcade.load_tilemap(str(map_path))

        # Позиция спавна игрока из слоя карты
        spawn_x, spawn_y = 0, 0
        spawn_layer = None

        # Пытаемся найти слой спавна по разным вариантам имени
        if hasattr(self.tile_map, "sprite_lists"):
            for layer_name in ("spawn", "Spawn", "player_spawn", "PlayerSpawn"):
                if layer_name in self.tile_map.sprite_lists:
                    spawn_layer = self.tile_map.sprite_lists[layer_name]
                    break

        if spawn_layer and len(spawn_layer) > 0:
            spawn_sprite = spawn_layer[0]
            spawn_x, spawn_y = spawn_sprite.center_x, spawn_sprite.center_y
        else:
            # Если слой спавна не найден, используем запасную позицию
            spawn_x, spawn_y = 300, 300

        # Игрок
        self.player = Player(spawn_x, spawn_y)
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Список объектов, которые можно перематывать
        # self.rewindable_objects = []  # логика
        # self.rewindable_objects_sprites = arcade.SpriteList()  # спрайты

        # Статичные платформы (берём слой collision из тайл-карты)
        self.static_platforms = arcade.SpriteList()
        if hasattr(self.tile_map, "sprite_lists"):
            for layer_name in ("collision", "Collision", "Collisions"):
                if layer_name in self.tile_map.sprite_lists:
                    self.static_platforms = self.tile_map.sprite_lists[layer_name]
                    break

        # Двигающиеся платформы
        self.moving_platforms = []
        self.moving_platform_sprites = arcade.SpriteList()

        # Управление
        self.input_manager = InputManager(self.player)
        # self.input_manager = InputManager(self.player, self.time_system,
        #                                   self.rewindable_objects)

        # Дополнительные слои карты
        if hasattr(self.tile_map, "sprite_lists") and "DeathZones" in self.tile_map.sprite_lists:
            self.death_zones = self.tile_map.sprite_lists["DeathZones"]
        else:
            self.death_zones = arcade.SpriteList()

        # Физика
        platforms = arcade.SpriteList()
        platforms.extend(self.static_platforms)
        platforms.extend(self.moving_platform_sprites)
        # platforms.extend(self.rewindable_objects_sprites)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=platforms,
            gravity_constant=0.5
        )

    # ОТРИСОВКА
    def on_draw(self):
        self.clear()

        self.camera.use()

        # Рисуем карту и объекты
        if self.tile_map and hasattr(self.tile_map, "sprite_lists"):
            for sprite_list in self.tile_map.sprite_lists.values():
                sprite_list.draw()

        # Двигающиеся платформы и игрок (не входят в sprite_lists карты)
        self.moving_platform_sprites.draw()
        self.player_list.draw()

        self.gui_camera.use()

    # ОБНОВЛЕНИЕ ЛОГИКИ
    def on_update(self, delta_time):
        self.input_manager.update(delta_time)
        self.physics_engine.update()

        # Камера следует за игроком с плавным смещением
        target_x, target_y = self.player.center_x, self.player.center_y
        current_x, current_y = self.camera.position
        lerp_speed = 0.1
        new_x = current_x + (target_x - current_x) * lerp_speed
        new_y = current_y + (target_y - current_y) * lerp_speed
        self.camera.position = (new_x, new_y)

        self.player.update_on_ground_state(self.physics_engine)
        self.player.update_animation(delta_time)

        if arcade.check_for_collision_with_list(self.player, self.death_zones):
            self.player.kill()

        for platform in self.moving_platforms:
            platform.update(delta_time)

    # INPUT
    def on_key_press(self, key, modifiers):
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        # Переводим экранные координаты мыши в мировые с учётом камеры
        world_pos = self.camera.unproject((x, y))
        self.input_manager.on_mouse_press(world_pos[0], world_pos[1], button, modifiers)
