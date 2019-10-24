class Settings:

    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 773
        self.player_speed = 10
        self.enemy_speed = 5
        self.ground_speed = 3
        self.chance_to_drop = 150
        self.chance_to_fire = 2
        self.bullet_speed = 15
        self.fps = 30
        self.player_start_ammo = 100

    def get_screen_size(self):
        return self.screen_width, self.screen_height
