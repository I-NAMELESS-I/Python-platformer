from pathlib import Path

import arcade

from code.time_system.time_system import TimeSystem

from code.core.input_manager import InputManager
from code.level.level_loader import LevelLoader
from code.settings import MAPS_DIR
from code.core.pause_view import PauseView


class GameView(arcade.View):
    def __init__(self, map_path: Path | str | None = None):
        super().__init__()

        # Камера для мира и для UI
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.camera.zoom = 2

        # Выбранный уровень
        self.map_path = Path(map_path) if map_path else MAPS_DIR / "test_map.tmx"

        # Загружаем данные уровня через загрузчик
        self.level_loader = LevelLoader(self.map_path)
        self.level_data = self.level_loader.load()

        self.tile_map = self.level_data.tile_map
        self.player = self.level_data.player
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        # Платформы
        self.static_platforms = self.level_data.static_platforms
        self.moving_platforms = self.level_data.moving_platforms
        self.rewindable_platforms = self.level_data.rewindable_platforms
        self.moving_platform_sprites = self.level_data.moving_all_platform_sprites

        # после self.rewindable_platforms = self.level_data.rewindable_platforms
        self.time_system = TimeSystem(self.rewindable_platforms)

        # перед созданием InputManager передаём time_system и список rewindable объектов
        self.input_manager = InputManager(self.player, time_system=self.time_system, rewindable_platforms=self.rewindable_platforms)

        # Дополнительные слои карты
        self.death_zones = self.level_data.death_zones or arcade.SpriteList()

        # Физика
        platforms = arcade.SpriteList()
        platforms.extend(self.static_platforms)
        platforms.extend(self.moving_platform_sprites)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            platforms=platforms,
            gravity_constant=0.5
        )

        # Центрируем камеру на старте
        self.camera.position = (self.player.center_x, self.player.center_y)

    # ОТРИСОВКА
    def on_draw(self):
        self.clear()

        self.camera.use()

        # Рисуем карту и объекты
        if self.tile_map and hasattr(self.tile_map, "sprite_lists"):
            for name, sprite_list in self.tile_map.sprite_lists.items():
                # Двигающиеся платформы рисуем отдельно, чтобы не дублировать
                if name in ("MovingPlatform", "moving_platform", "MovingPlatforms", "RewindablePlatforms"):
                    continue
                sprite_list.draw()

        # Двигающиеся платформы и игрок (не входят в sprite_lists карты)
        self.moving_platform_sprites.draw()
        self.player_list.draw()

        self.gui_camera.use()

    # ОБНОВЛЕНИЕ ЛОГИКИ
    def on_update(self, delta_time):
        self.input_manager.update(delta_time)
        self.time_system.update(delta_time)
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
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))
            return
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        # Переводим экранные координаты мыши в мировые с учётом камеры
        world_pos = self.camera.unproject((x, y))
        self.input_manager.on_mouse_press(world_pos[0], world_pos[1], button, modifiers)
