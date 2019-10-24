import random
import pygame
from pygame.sprite import Sprite


class Penguin:

    def __init__(self, settings, x, y, images):
        """

        :param x: (imt) coordinate to spawn
        :param y: (int) coordinate to spawn
        :param images: (list) faced forward penguin images [needed to get collision mask and make animations]
        """
        self.settings = settings
        self.x = x
        self.y = y
        self.img_count = 0
        self.images = images
        self.lives = 1
        self.width = 78
        self.height = 73
        self.bg_width = settings.screen_width
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

    def draw(self, win):
        if self.img_count > 15:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        win.blit(self.images[self.img_count], (self.x, self.y))

        self.img_count += 1


class Player(Penguin):

    def __init__(self, settings, x, y, images, reversed_images):
        super().__init__(settings, x, y, images)
        self.reversed_images = reversed_images
        self.lives = 2
        self.score = 0
        self.ammo = self.settings.player_start_ammo

    def update(self):
        if self.move_right and self.x < (1024 - self.width):
            self.x += self.settings.player_speed
        if self.move_left and self.x > 0:
            self.x -= self.settings.player_speed
        if self.move_up and self.y > 610 - self.height:
            self.y -= self.settings.player_speed
        if self.move_down and self.y < 630:
            self.y += self.settings.player_speed

    def has_ammo(self):
        return self.ammo > 0

    def draw(self, win):
        if self.img_count > 15:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        if self.move_left:
            win.blit(self.reversed_images[self.img_count], (self.x, self.y))
        else:
            win.blit(self.images[self.img_count], (self.x, self.y))

        self.img_count += 1

    def get_mask(self):
        """
        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        if self.move_left:
            return pygame.mask.from_surface(self.reversed_images[self.img_count])

        return pygame.mask.from_surface(self.images[self.img_count])


class Enemy(Penguin):
    def __init__(self, settings, x, y, reversed_images):
        super().__init__(settings, x, y, reversed_images)
        self.reversed_images = reversed_images
        self.lives = 1
        self.move_left = True

    def update(self):
        if self.x > 0:
            self.x -= self.settings.enemy_speed

    def fire(self, bullet_list, projectile):
        if self.x < self.bg_width and random.randint(1, 100) < self.settings.chance_to_fire:
            bullet_list.add(projectile)

    def chance_to_drop(self, chance):
        return random.randint(1, 100) < chance

    def get_mask(self):
        """
        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        return pygame.mask.from_surface(self.reversed_images[self.img_count])
