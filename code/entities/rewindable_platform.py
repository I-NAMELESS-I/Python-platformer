import arcade
from typing import Optional

class RewindablePlatform:
    # Читаем свойства vx, vy из tmx в level_loader, потом саму платфому уже передаем в game_view
    def __init__(
            self, sprite: arcade.Sprite, 
            vx: float = 0.0, vy: float = 0.0, 
            boundary_left: Optional[float] = None, 
            boundary_right: Optional[float] = None, 
            boundary_top: Optional[float] = None, 
            boundary_bottom: Optional[float] = None, 
        ):
        self.sprite = sprite
        self.vx = vx
        self.vy = vy

        # Сохраняем "исходную" скорость, чтобы при rewind инвертировать её
        self.original_vx = vx
        self.original_vy = vy

        self.paused = False
        self.rewinding = False

        self.is_selected = False

        # Границы движения, если заданы в свойствах карты
        self.boundary_left = boundary_left
        self.boundary_right = boundary_right
        self.boundary_top = boundary_top
        self.boundary_bottom = boundary_bottom

        self.sprite.update = lambda: None

    def start_pause(self):
        if not self.paused:
            self.paused = True
    
    def stop_pause(self):
        if self.paused:
            self.paused = False

    def start_rewind(self):
        if not self.rewinding:
            self.rewinding = True
    
    def stop_rewind(self):
        if self.rewinding:
            self.rewinding = False

    def update(self, delta_time: float):
        if self.paused:
            return

        if self.rewinding:
            dx = -self.vx * delta_time
            dy = -self.vy * delta_time
        else:
            dx = self.vx * delta_time
            dy = self.vy * delta_time

        # Перемещаем спрайт вручную
        self.sprite.center_x += dx
        self.sprite.center_y += dy

        # Проверка и обработка границ по X
        if self.boundary_left is not None and self.sprite.center_x < self.boundary_left:
            self.sprite.center_x = self.boundary_left
            self.vx *= -1

        if self.boundary_right is not None and self.sprite.center_x > self.boundary_right:
            self.sprite.center_x = self.boundary_right
            self.vx *= -1

        # Проверка и обработка границ по Y
        if self.boundary_bottom is not None and self.sprite.center_y < self.boundary_bottom:
            self.sprite.center_y = self.boundary_bottom
            self.vy *= -1

        if self.boundary_top is not None and self.sprite.center_y > self.boundary_top:
            self.sprite.center_y = self.boundary_top
            self.vy *= -1
