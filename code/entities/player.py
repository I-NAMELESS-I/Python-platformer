import arcade


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.idle_textures = []
        for i in range(7):
            texture = arcade.load_texture(f"assets/sprites/player/idle/idle{i}.png")
            self.idle_textures.append(texture)

        self.current_texture = 0
        self.texture_change_time = 0
        self.texture_change_delay = 0.1
        self.is_walking = False

    def update_animation(self, delta_time: float = 1 / 60):
        """ Обновление анимации """
        if self.is_walking:
            # self.texture_change_time += delta_time
            # if self.texture_change_time >= self.texture_change_delay:
            #     self.texture_change_time = 0
            #     self.current_texture += 1
            #     if self.current_texture >= len(self.walk_textures):
            #         self.current_texture = 0
            #     self.texture = self.walk_textures[self.current_texture]
            ...
        else:
            self.texture_change_time += delta_time
            if self.texture_change_time >= self.texture_change_delay:
                self.texture_change_time = 0
                self.current_texture += 1
                if self.current_texture >= len(self.idle_textures):
                    self.current_texture = 0
                self.texture = self.idle_textures[self.current_texture]
