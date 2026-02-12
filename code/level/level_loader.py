from pathlib import Path
from typing import List, Optional

import arcade

from code.entities.player import Player
from code.entities.rewindable_platform import RewindablePlatform
from code.entities.moving_platform import MovingPlatform


class LevelData:
    def __init__(self):
        self.tile_map: Optional[arcade.TileMap] = None
        self.player: Optional[Player] = None

        # Спрайтлисты для отрисовки / физики
        self.static_platforms: arcade.SpriteList = arcade.SpriteList()
        self.moving_all_platform_sprites: arcade.SpriteList = arcade.SpriteList()
        self.death_zones: arcade.SpriteList = arcade.SpriteList()

        # Объекты с логикой
        self.moving_platforms: List[MovingPlatform] = []
        self.rewindable_platforms: List[RewindablePlatform] = []


class LevelLoader:
    """
    Загружает уровень из TMX и возвращает LevelData.
    Ожидаемые имена слоёв в TMX:
      - Collision  (статичные платформы для physics)
      - MovingPlatform  (объекты-платформы с properties)
      - RewindablePlatforms (объекты которые можно перемотать)
      - Spawn или PlayerSpawn  (точка спавна игрока)
      - DeathZones  (зоны смерти / шипы)
    Ожидаемые свойства объекта платформы:
      - cl_x, cl_y  (скорость в пикселях в секунду)
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
        if hasattr(data.tile_map, "sprite_lists"):
            for layer_name in ("spawn", "Spawn", "player_spawn", "PlayerSpawn"):
                if layer_name in data.tile_map.sprite_lists:
                    spawn_layer = data.tile_map.sprite_lists[layer_name]
                    break

        if spawn_layer and len(spawn_layer) > 0:
            spawn_sprite = spawn_layer[0]
            spawn_x, spawn_y = spawn_sprite.center_x, spawn_sprite.center_y
        else:
            # Если слой спавна не найден, используем запасную позицию
            spawn_x, spawn_y = 300, 300

        data.player = Player(spawn_x, spawn_y)

        # 4. platforms
        moving_layers = []

        # Явный слой для rewindable
        if "RewindablePlatforms" in data.tile_map.sprite_lists:
            moving_layers.append(("RewindablePlatforms", data.tile_map.sprite_lists["RewindablePlatforms"]))

        # Обычные движущиеся платформы
        for name in ("MovingPlatform",):
            if name in data.tile_map.sprite_lists:
                moving_layers.append((name, data.tile_map.sprite_lists[name]))

        # Обрабатываем все найденные слои
        for layer_name, sprite_list in moving_layers:
            for spr in sprite_list:
                props = getattr(spr, "properties", {}) or {}

                # скорости
                vx = float(props.get("cl_x", props.get("vx", 0)))
                vy = float(props.get("cl_y", props.get("vy", 0)))

                # границы
                left = self._parse_float(props.get("boundary_left"))
                right = self._parse_float(props.get("boundary_right"))
                top = self._parse_float(props.get("boundary_top"))
                bottom = self._parse_float(props.get("boundary_bottom"))

                # rewindable?
                rewindable_flag = self._parse_bool(props.get("rewindable"))
                if layer_name == "RewindablePlatforms":
                    rewindable_flag = True

                # создаём объект
                if rewindable_flag:
                    obj = RewindablePlatform(
                        spr,
                        vx=vx, vy=vy,
                        boundary_left=left,
                        boundary_right=right,
                        boundary_top=top,
                        boundary_bottom=bottom
                    )
                    data.rewindable_platforms.append(obj)
                else:
                    obj = MovingPlatform(
                        spr,
                        vx=vx, vy=vy,
                        boundary_left=left,
                        boundary_right=right,
                        boundary_top=top,
                        boundary_bottom=bottom
                    )
                    data.moving_platforms.append(obj)

                # общий список спрайтов
                data.moving_all_platform_sprites.append(spr)

        return data

    def _parse_bool(self, value):
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        # Числа
        if isinstance(value, (int, float)):
            return value != 0

        # Строки
        s = str(value).strip().lower()
        return s in ("1", "true", "yes", "y", "on")
    
    def _parse_float(self, value):
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

