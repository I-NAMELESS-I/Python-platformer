import arcade
from typing import Optional


class MovingPlatform:
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

        self.original_vx = vx
        self.original_vy = vy

    def update(self, delta_time: float):
        dx = self.vx * delta_time
        dy = self.vy * delta_time

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
