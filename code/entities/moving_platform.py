import arcade

class MovingPlatform:
    # Простая платформа с постоянной скоростью и границами (как вспомогательный объект который может пригодиться)

    def __init__(self, sprite: arcade.Sprite, vx: float = 0.0, vy: float = 0.0, dx: float = 0.0, dy: float = 0.0):
        self.sprite = sprite
        self.vx = vx
        self.vy = vy
        self.start_x = float(sprite.center_x)
        self.start_y = float(sprite.center_y)
        self.dx = float(dx)
        self.dy = float(dy)

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

        self.last_dx = 0.0
        self.last_dy = 0.0

    def update(self, delta_time: float):
        old_x = float(self.sprite.center_x)
        old_y = float(self.sprite.center_y)

        new_x = old_x + self.vx * delta_time
        new_y = old_y + self.vy * delta_time

        if self.boundary_left is not None and new_x < self.boundary_left:
            new_x = self.boundary_left
            self.vx *= -1
        if self.boundary_right is not None and new_x > self.boundary_right:
            new_x = self.boundary_right
            self.vx *= -1

        if self.boundary_bottom is not None and new_y < self.boundary_bottom:
            new_y = self.boundary_bottom
            self.vy *= -1
        if self.boundary_top is not None and new_y > self.boundary_top:
            new_y = self.boundary_top
            self.vy *= -1

        self.sprite.center_x = new_x
        self.sprite.center_y = new_y

        self.last_dx = new_x - old_x
        self.last_dy = new_y - old_y
