from pathlib import Path
from typing import List, Optional

import arcade

from code.entities.player import Player
from code.entities.rewindable_platform import RewindablePlatform
from code.settings import SPRITES_DIR


class LevelData:
    def __init__(self):
        self.tile_map: Optional[arcade.TileMap] = None
        self.player: Optional[Player] = None

        # Спрайтлисты для отрисовки / физики
        self.static_platforms: arcade.SpriteList = arcade.SpriteList()
        self.moving_all_platform_sprites: arcade.SpriteList = arcade.SpriteList()
        self.death_zones: arcade.SpriteList = arcade.SpriteList()

        # Объекты с логикой
        self.moving_platforms: List[RewindablePlatform] = []
        self.rewindable_objects: List[RewindablePlatform] = []


class LevelLoader:
    """
    Загружает уровень из TMX и возвращает LevelData.
    Ожидаемые имена слоёв в TMX:
      - Collision  (статичные платформы для physics)
      - MovingPlatforms  (объекты-платформы с properties)
      - Spawn или PlayerSpawn  (точка спавна игрока)
      - DeathZones  (зоны смерти / шипы)
    Ожидаемые свойства объекта платформы:
      - change_x, change_y  (скорость в пикселях в секунду)
      - boundary_left, boundary_right, boundary_top, boundary_bottom  (границы движения)
      - rewindable  (boolean)
    """
    def __init__(self, map_path: Path):
        self.map_path = map_path

    def load(self) -> LevelData:
        data = LevelData()

        # Загружаем тайлкарту
        data.tile_map = arcade.load_tilemap(str(self.map_path))

        # 1. Статичные платформы (Collision)
        if hasattr(data.tile_map, "sprite_lists"):
            for name in ("Collision", "collision", "Collisions"):
                if name in data.tile_map.sprite_lists:
                    data.static_platforms = data.tile_map.sprite_lists[name]
                    break

        # 2. Death zones / spikes
        if hasattr(data.tile_map, "sprite_lists") and "DeathZones" in data.tile_map.sprite_lists:
            data.death_zones = data.tile_map.sprite_lists["DeathZones"]

        # 3. Player spawn
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

        data.player = Player(spawn_x, spawn_y)

        # 4. Moving platforms (пока только которые можно перемотать)
        if hasattr(data.tile_map, "sprite_lists") and "MovingPlatforms" in data.tile_map.sprite_lists:
            mp_list = data.tile_map.sprite_lists["MovingPlatforms"]
            for spr in mp_list:
                props = getattr(spr, "properties", {}) or {}

                # читаем скорости (поддерживаем разные имена)
                vx = float(props.get("change_x", props.get("vx", 0)))
                vy = float(props.get("change_y", props.get("vy", 0)))

                # создаём объект-обёртку
                rp = RewindablePlatform(spr, vx=vx, vy=vy)

                # читаем границы, если заданы
                left = props.get("boundary_left")
                right = props.get("boundary_right")
                top = props.get("boundary_top")
                bottom = props.get("boundary_bottom")

                rp.boundary_left = float(left) if left is not None else None
                rp.boundary_right = float(right) if right is not None else None
                rp.boundary_top = float(top) if top is not None else None
                rp.boundary_bottom = float(bottom) if bottom is not None else None

                # rewindable флаг
                rewindable_flag = props.get("rewindable", False)
                if isinstance(rewindable_flag, str):
                    rewindable_flag = rewindable_flag.lower() in ("1", "true", "yes")
                
                data.rewindable_objects.append(rp)
                data.moving_all_platform_sprites.append(spr)

        return data
