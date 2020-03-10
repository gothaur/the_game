import pygame
from pygame.sprite import Sprite
from penguin import Enemy


class Projectile(Sprite):

    def __init__(self, settings, penguin, f_img, b_img):
        """
        :param penguin: penguin which fired projectile
        :param f_img: image faced forward
        :param b_img: image faced backward
        """
        super().__init__()
        self.direction = penguin.move_left
        if self.direction:
            self.width = b_img.get_width()
            self.height = b_img.get_height()
        else:
            self.width = f_img.get_width()
            self.height = f_img.get_height()
        if self.direction or type(penguin) == Enemy:
            self.x = penguin.x - int(penguin.get_width() * 0.35)
        else:
            self.x = penguin.x + int(penguin.get_height())
        self.y = penguin.y + int(penguin.get_width() * 0.25)
        self.penguin = penguin
        self.f_img = f_img
        self.b_img = b_img
        self.settings = settings
        self.name = "Projectile"

    def draw(self, win):
        """
        Draws projectile on the screen
        :return: None
        """
        if self.direction or type(self.penguin) == Enemy:
            image = self.b_img
        else:
            image = self.f_img
        win.blit(image, (self.x, self.y))

    def move(self):
        """
        Moves projectile on the screen
        :return: None
        """
        if self.direction or type(self.penguin) == Enemy:
            self.x -= (self.penguin.get_vel() + self.settings.bullet_speed)
        else:
            self.x += self.penguin.get_vel() + 15 + self.settings.bullet_speed

    def collide(self, penguin):
        """
        Checks if projectile collides with penguin
        :param penguin:
        :return: True if collided
        """
        penguin_mask = penguin.get_mask()
        if self.direction or type(penguin) == Enemy:
            projectile_mask = pygame.mask.from_surface(self.b_img)
        else:
            projectile_mask = pygame.mask.from_surface(self.f_img)

        offset = (self.x - penguin.get_x(), self.y - penguin.get_y())
        return penguin_mask.overlap(projectile_mask, offset)
