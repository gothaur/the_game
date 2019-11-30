import random
import pygame
import time


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
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        self.bg_width = settings.screen_width
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.battlefield_bottom = self.settings.ground_bottom - self.height
        self.battlefield_top = self.battlefield_bottom - settings.battlefield_height

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

    def is_dead(self):
        return self.lives <= 0

    def draw(self, win):
        self.img_count += 1
        if self.img_count > 16 * self.settings.fps_multipler:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        win.blit(self.images[int(self.img_count / self.settings.fps_multipler)], (self.x, self.y))


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
        if self.move_up and self.y > self.battlefield_top:
            self.y -= self.settings.player_speed
        if self.move_down and self.y < self.battlefield_bottom:
            self.y += self.settings.player_speed

    def has_ammo(self):
        return self.ammo > 0

    def draw(self, win):
        self.img_count += 1
        if self.img_count > 16 * self.settings.fps_multipler:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        if self.move_left:
            win.blit(self.reversed_images[int(self.img_count / self.settings.fps_multipler)], (self.x, self.y))
        else:
            win.blit(self.images[int(self.img_count / self.settings.fps_multipler)], (self.x, self.y))

    def get_mask(self):
        """
        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        if self.move_left:
            return pygame.mask.from_surface(self.reversed_images[int(self.img_count / self.settings.fps_multipler)])

        return pygame.mask.from_surface(self.images[int(self.img_count / self.settings.fps_multipler)])


class Enemy(Penguin):
    def __init__(self, settings, x, y, reversed_images):
        super().__init__(settings, x, y, reversed_images)
        self.reversed_images = reversed_images
        self.lives = 1
        self.move_left = True
        self.chance_to_drop = random.randint(1, 100) < settings.chance_to_drop
        self.last_shot = time.time()
        self.time_to_fire = 0

    def update(self):
        if self.x > 0:
            self.x -= self.settings.enemy_speed

    def fire(self, bullet_list, projectile):
        current_time = time.time()
        self.time_to_fire = current_time - self.last_shot > self.settings.shoots_delay
        if self.time_to_fire and self.x < self.bg_width and random.randint(1, 100) < self.settings.chance_to_fire:
            self.last_shot = time.time()
            bullet_list.add(projectile)

    def get_mask(self):
        """
        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        return pygame.mask.from_surface(self.reversed_images[int(self.img_count / self.settings.fps_multipler)])
