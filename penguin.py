import random
import pygame


class Penguin:

    def __init__(self, x, y, bg_width, p_images, lives=1, enemy=False):
        """

        :param x: coordinate to spawn
        :param y: coordinate to spawn
        :param bg_width: width of the screen
        :param p_images: penguin images [needed to get collision mask]
        :param p_sheet: penguin image sheet [needed to animate penguin on screen]
        :param coord: coords each image on sheet
        :param lives: how many lives penguin has
        :param enemy: if penguin is enemy or player
        """
        self.x = x
        self.y = y
        self.vel_forward = 5
        self.vel_backward = 3
        self.img_count = 0
        self.img = p_images[0]
        self. p_images = p_images
        self.width = 78
        self.height = 73
        self.lives = lives
        self.moving_backward = False
        self.enemy = enemy
        self.is_moving = False
        self.bg_width = bg_width
        self.name = 'Penguin'
        if not enemy:
            self.ammo = 10
        self.name = "Penguin"

    def get_vel(self):
        return self.vel_forward

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
        if self.enemy and self.x < self.bg_width and random.randint(1, 100) < -5:
            bullet_list.append(projectile)

    def chance_to_drop(self):
        return random.randint(1, 100) < 150

    def move(self, key):
        if self.enemy:
            if self.x > 0:
                self.x -= 8
        else:
            self.moving_backward = False
            self.is_moving = False
            if key[pygame.K_UP] and self.y > 610 - self.height:
                self.y -= 5
            if key[pygame.K_DOWN] and self.y < 630:
                self.y += 5
            if key[pygame.K_LEFT] and self.x > 0:
                self.x -= self.vel_backward
                self.moving_backward = True
                self.is_moving = True
            if key[pygame.K_RIGHT] and self.x < (1024 - self.width):
                self.is_moving = True
                self.x += self.vel_forward

    def draw(self, win):
        if self.img_count > 15:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        if self.moving_backward or self.enemy:
            win.blit(pygame.transform.flip(self.p_images[self.img_count], True, False), (self.x, self.y))
        else:
            win.blit(self.p_images[self.img_count], (self.x, self.y))

        self.img_count += 1

    def get_mask(self):
        """
        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        return pygame.mask.from_surface(self.p_images[self.img_count])
