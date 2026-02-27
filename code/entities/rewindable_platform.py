import arcade
from typing import Optional

class RewindablePlatform:
    # Платформа с поддержкой паузы и перемотки.

    def __init__(
        self,
        sprite: arcade.Sprite,
        vx: float = 0.0,
        vy: float = 0.0,
        dx: float = 0.0,
        dy: float = 0.0,
    ):
        self.sprite = sprite
        self.vx = vx
        self.vy = vy

        # движене в пределах границ: dx/dy — относительное смещение от начальной позиции
        self.start_x = float(self.sprite.center_x)
        self.start_y = float(self.sprite.center_y)
        self.dx = float(dx)
        self.dy = float(dy)

        # вычисление границ
        if self.dx != 0.0:
            x1 = self.start_x
            x2 = self.start_x + self.dx
            self.boundary_left = min(x1, x2)
            self.boundary_right = max(x1, x2)
        else:
            self.boundary_left = None
            self.boundary_right = None

        if self.dy != 0.0:
            y1 = self.start_y
            y2 = self.start_y + self.dy
            self.boundary_bottom = min(y1, y2)
            self.boundary_top = max(y1, y2)
        else:
            self.boundary_bottom = None
            self.boundary_top = None

        self.paused = False
        self.rewinding = False

        # смещение, применённое в последнем update (для переноса игрока)
        self.last_dx = 0.0
        self.last_dy = 0.0

    def start_pause(self):
        self.paused = True

    def stop_pause(self):
        self.paused = False

    def start_rewind(self):
        self.rewinding = True

    def stop_rewind(self):
        self.rewinding = False

    def update(self, delta_time: float):
        # по умолчанию — нулевое смещение
        self.last_dx = 0.0
        self.last_dy = 0.0

        if self.paused:
            return

        vx = -self.vx if self.rewinding else self.vx
        vy = -self.vy if self.rewinding else self.vy

        old_x = float(self.sprite.center_x)
        old_y = float(self.sprite.center_y)

        intended_dx = vx * delta_time
        intended_dy = vy * delta_time

        new_x = old_x + intended_dx
        new_y = old_y + intended_dy

        # корректируем по границам и при необходимости инвертируем скорость
        if self.boundary_left is not None and new_x < self.boundary_left:
            new_x = self.boundary_left
            self.vx = -self.vx
        if self.boundary_right is not None and new_x > self.boundary_right:
            new_x = self.boundary_right
            self.vx = -self.vx

        if self.boundary_bottom is not None and new_y < self.boundary_bottom:
            new_y = self.boundary_bottom
            self.vy = -self.vy
        if self.boundary_top is not None and new_y > self.boundary_top:
            new_y = self.boundary_top
            self.vy = -self.vy

        # применяем позицию и считаем фактическое смещение
        self.sprite.center_x = new_x
        self.sprite.center_y = new_y

        self.last_dx = new_x - old_x
        self.last_dy = new_y - old_y

