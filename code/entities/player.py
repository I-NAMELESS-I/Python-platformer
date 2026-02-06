import arcade

from code.settings import SPRITES_DIR


class Player(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.center_x = x
        self.center_y = y

        # Параметры движения
        self.move_speed = 5
        self.jump_speed = 8
        self.fast_fall_speed = -12  # импульс для быстрого падения
        self.on_ground = False

        # Направление движения (1 — вправо, -1 — влево)
        self.facing = 1

        # Анимация
        self.cur_texture = 0
        self.animation_speed = 0.2
        self.animation_state = "idle"  # "idle", "run", "jump"

        self.idle_textures = []
        idle_dir = SPRITES_DIR / "player" / "idle"
        for i in range(7):
            self.idle_textures.append(
                arcade.load_texture(idle_dir / f"idle{i}.png")
            )

        self.run_textures = []
        run_dir = SPRITES_DIR / "player" / "run"
        for i in range(6):
            self.run_textures.append(
                arcade.load_texture(run_dir / f"run{i}.png")
            )

        self.jump_texture = []
        jump_dir = SPRITES_DIR / "player" / "jump"
        for i in range(6):
            self.jump_texture.append(
                arcade.load_texture(jump_dir / f"jump{i}.png")
            )

        self.texture = self.idle_textures[0]

    def move_left(self):
        self.change_x = -self.move_speed
        self.facing = -1

    def move_right(self):
        self.change_x = self.move_speed
        self.facing = 1

    def stop_horizontal(self):
        self.change_x = 0

    def jump(self):
        if self.on_ground:
            self.change_y = self.jump_speed
            self.on_ground = False

    def fast_fall(self):
        if not self.on_ground:
            # Разовый сильный импульс вниз, дальше управляет гравитация физмотора
            self.change_y = self.fast_fall_speed

    def update_on_ground_state(self, physics_engine):
        self.on_ground = physics_engine.can_jump()

    def update_animation(self, dt):
        # Определяем текущее состояние анимации
        if not self.on_ground:
            state = "jump"
        elif abs(self.change_x) > 0:
            state = "run"
        else:
            state = "idle"

        # Если состояние сменилось (jump -> run -> idle и т.п.), сбрасываем кадр
        if state != self.animation_state:
            self.animation_state = state
            self.cur_texture = 0

        # Продвигаем кадр
        self.cur_texture += self.animation_speed

        if state == "jump":
            if self.cur_texture >= len(self.jump_texture):
                self.cur_texture = 0
            tex = self.jump_texture[int(self.cur_texture)]
        elif state == "run":
            if self.cur_texture >= len(self.run_textures):
                self.cur_texture = 0
            tex = self.run_textures[int(self.cur_texture)]
        else:  # idle
            if self.cur_texture >= len(self.idle_textures):
                self.cur_texture = 0
            tex = self.idle_textures[int(self.cur_texture)]

        self.texture = tex
        if self.facing == -1:
            self.texture = tex.flip_left_right()

    def kill(self):
        pass
