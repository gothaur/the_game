class Settings:

    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 773
        self.player_speed = 6
        self.enemy_speed = 5
        self.ground_speed = 3
        self.chance_to_drop = 25
        self.chance_to_fire = 25
        self.chance_to_drop_ammo = 75
        self.chance_to_drop_health = 20
        self.chance_to_drop_present = 5
        self.chance_to_drop_mine = 5
        self.bullet_speed = 7
        self.fps_multipler = 2  # all game aspects were tested with multipler set to 2 (Change this for your own risk)
        self.player_start_ammo = 100
        self.shoots_delay = 1  # how many second have to pass before next shoot
        self.max_enemy_bullets = 4  # defines how many bullets can all enemy shot at once
        self.max_player_bullets = 2  # defines how many shots can player takes

    def get_screen_size(self):
        return self.screen_width, self.screen_height
