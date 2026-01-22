import arcade


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Позиция
        self.center_x = x
        self.center_y = y

        # Скорости
        self.move_speed = 5
        self.jump_speed = 10
        self.fast_fall_speed = -10

        # Флаг "на земле"
        self.on_ground = False

        # Направление (1 = вправо, -1 = влево)
        self.facing = 1

        # Анимация
        self.cur_texture = 0
        self.animation_speed = 0.2

        # Загружаем текстуры
        self.idle_textures = []
        for i in range(7):
            self.idle_textures.append(arcade.load_texture(f"assets/sprites/player/idle/idle{i}.png"))

        self.run_textures = []
        for i in range(6):
            self.idle_textures.append(arcade.load_texture(f"assets/sprites/player/run/run{i}.png"))

        self.jump_texture = []
        for i in range(6):
            self.idle_textures.append(arcade.load_texture(f"assets/sprites/player/jump/jump{i}.png"))

        # С ней пока не знаю че делать
        self.fall_texture = arcade.load_texture("assets/sprites/player/fall/fall.png")

        # Начальная текстура
        self.texture = self.idle_textures[0]

    # ДВИЖЕНИЕ
    def move_left(self):
        self.change_x = -self.move_speed
        self.facing = -1

    def move_right(self):
        self.change_x = self.move_speed
        self.facing = 1

    def stop_horizontal(self):
        self.change_x = 0

    # ПРЫЖОК
    def jump(self):
        if self.on_ground:
            self.change_y = self.jump_speed
            self.on_ground = False

    # БЫСТРОЕ ПАДЕНИЕ
    def fast_fall(self):
        if not self.on_ground:
            self.change_y = self.fast_fall_speed

    # ОБНОВЛЕНИЕ ФЛАГА ON_GROUND
    def update_on_ground_state(self, physics_engine):
        self.on_ground = physics_engine.can_jump()

    # АНИМАЦИЯ
    def update_animation(self, dt):
        # Прыжок
        if not self.on_ground:
            tex = self.jump_texture if self.change_y > 0 else self.fall_texture
            self.texture = arcade.load_texture(
                tex.file_name,
                flipped_horizontally=(self.facing == -1)
            )
            return

        # Бег
        if abs(self.change_x) > 0:
            self.cur_texture += self.animation_speed
            if self.cur_texture >= len(self.run_textures):
                self.cur_texture = 0

            tex = self.run_textures[int(self.cur_texture)]
            self.texture = arcade.load_texture(
                tex.file_name,
                flipped_horizontally=(self.facing == -1)
            )
            return

        # Idle
        self.cur_texture += self.animation_speed
        if self.cur_texture >= len(self.idle_textures):
            self.cur_texture = 0

        tex = self.idle_textures[int(self.cur_texture)]
        self.texture = arcade.load_texture(
            tex.file_name,
            flipped_horizontally=(self.facing == -1)
        )

    def kill(self):
        pass