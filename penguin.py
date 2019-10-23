import random
import pygame


class Penguin:

    def __init__(self, settings, x, y, bg_width, f_images, b_images, lives=1, enemy=False):
        """

        :param x: (imt) coordinate to spawn
        :param y: (int) coordinate to spawn
        :param bg_width: (int) width of the screen
        :param f_images: (list) faced forward penguin images [needed to get collision mask and make animations]
        :param b_images: (list) faced backward penguin images [needed to get collision mask and make animations]
        :param lives: (int) how many lives penguin has [enemy default has one, player two
        :param enemy: (bool) if penguin is enemy or player
        """
        self.x = x
        self.y = y
        self.img_count = 0
        self.f_images = f_images
        self.b_images = b_images
        self.width = 78
        self.height = 73
        self.lives = lives
        self.enemy = enemy
        self.bg_width = bg_width
        self.settings = settings
        if not enemy:
            self.ammo = self.settings.player_start_ammo
        self.score = 0
        self.name = "Penguin"
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def get_vel(self):
        return self.settings.player_speed

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def is_alive(self):
        return self.lives > 0

    def has_ammo(self):
        return self.ammo > 0

    def fire(self, bullet_list, projectile):
        if self.enemy and self.x < self.bg_width and random.randint(1, 100) < self.settings.chance_to_fire:
            bullet_list.append(projectile)

    def chance_to_drop(self, chance):
        return random.randint(1, 100) < chance

    def update_enemy(self):
        if self.enemy and self.x > 0:
            self.x -= self.settings.enemy_speed

    def update_player(self):
        if self.move_right and self.x < (1024 - self.width):
            self.x += self.settings.player_speed
        if self.move_left and self.x > 0:
            self.x -= self.settings.player_speed
        if self.move_up and self.y > 610 - self.height:
            self.y -= self.settings.player_speed
        if self.move_down and self.y < 630:
            self.y += self.settings.player_speed

    def draw(self, win):
        if self.img_count > 15:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        if self.move_left or self.enemy:
            win.blit(self.b_images[self.img_count], (self.x, self.y))
        else:
            win.blit(self.f_images[self.img_count], (self.x, self.y))

        self.img_count += 1

    def get_mask(self):
        """
        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        if self.move_left or self.enemy:
            return pygame.mask.from_surface(self.b_images[self.img_count])

        return pygame.mask.from_surface(self.f_images[self.img_count])
