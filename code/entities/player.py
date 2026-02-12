import arcade

from code.settings import SPRITES_DIR

class Player(arcade.Sprite):

    def __init__(self, x, y, on_death_complete=None):
        super().__init__()

        self.center_x = x
        self.center_y = y

        # Параметры движения
        self.move_speed = 5
        self.jump_speed = 8
        self.fast_fall_speed = -12
        self.on_ground = False

        # Направление движения (1 — вправо, -1 — влево)
        self.facing = 1

        # Анимация
        self.cur_texture = 0.0
        self.animation_speed = 0.2
        self.animation_state = "idle"  # "idle", "run", "jump"

        self.idle_textures = []
        idle_dir = SPRITES_DIR / "player" / "idle"
        for i in range(7):
            self.idle_textures.append(arcade.load_texture(idle_dir / f"idle{i}.png"))

        self.run_textures = []
        run_dir = SPRITES_DIR / "player" / "run"
        for i in range(6):
            self.run_textures.append(arcade.load_texture(run_dir / f"run{i}.png"))

        self.jump_texture = []
        jump_dir = SPRITES_DIR / "player" / "jump"
        for i in range(6):
            self.jump_texture.append(arcade.load_texture(jump_dir / f"jump{i}.png"))

        self.death_textures = []
        death_dir = SPRITES_DIR / "player" / "death"
        for i in range(7):
            self.death_textures.append(arcade.load_texture(death_dir / f"death{i}.png"))

        self.texture = self.idle_textures[0]

        self.dead = False
        self._death_frame = 0.0
        self._death_speed = 0.15
        self.on_death_complete = on_death_complete

    def move_left(self):
        if self.dead:
            return
        self.change_x = -self.move_speed
        self.facing = -1

    def move_right(self):
        if self.dead:
            return
        self.change_x = self.move_speed
        self.facing = 1

    def stop_horizontal(self):
        if self.dead:
            return
        self.change_x = 0

    def jump(self):
        if self.dead:
            return
        if self.on_ground:
            self.change_y = self.jump_speed
            self.on_ground = False

    def fast_fall(self):
        if self.dead:
            return
        if not self.on_ground:
            self.change_y = self.fast_fall_speed

    def update_on_ground_state(self, physics_engine):
        self.on_ground = physics_engine.can_jump()

    # kill запускет анимацию смерти
    def kill(self):
        if self.dead:
            return
        self.dead = True
        self._death_frame = 0.0
        # Остановить движение
        self.change_x = 0
        self.change_y = 0

    def update_animation(self, dt):
        # Если игрок мёртв — проигрываем анимацию смерти
        if self.dead:
            self._death_frame += self._death_speed
            idx = int(self._death_frame)
            if idx >= len(self.death_textures):
                # анимация закончилась, оставляем последний кадр и вызываем callback
                self.texture = self.death_textures[-1]
                if callable(self.on_death_complete):
                    cb = self.on_death_complete
                    self.on_death_complete = None
                    cb(self)
                return
            tex = self.death_textures[idx]
            self.texture = tex.flip_left_right() if self.facing == -1 else tex
            return

        if not self.on_ground:
            state = "jump"
        elif abs(self.change_x) > 0:
            state = "run"
        else:
            state = "idle"

        if state != self.animation_state:
            self.animation_state = state
            self.cur_texture = 0.0

        self.cur_texture += self.animation_speed

        if state == "jump":
            if self.cur_texture >= len(self.jump_texture):
                self.cur_texture = 0.0
            tex = self.jump_texture[int(self.cur_texture)]
        elif state == "run":
            if self.cur_texture >= len(self.run_textures):
                self.cur_texture = 0.0
            tex = self.run_textures[int(self.cur_texture)]
        else:  # idle
            if self.cur_texture >= len(self.idle_textures):
                self.cur_texture = 0.0
            tex = self.idle_textures[int(self.cur_texture)]

        self.texture = tex.flip_left_right() if self.facing == -1 else tex
