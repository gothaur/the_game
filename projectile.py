import pygame


class Projectile:

    def __init__(self, penguin, img):
        """

        :param penguin: penguin who fired or dropped object
        :param loot: type bool determinate if can buff player
        """
        self.direction = penguin.moving_backward
        if self.direction or penguin.enemy:
            self.x = penguin.x - 10
        else:
            self.x = penguin.x + penguin.get_height()
        self.y = int(penguin.y + penguin.get_width() / 2)
        self.penguin = penguin
        self.img = img

    def draw(self, win):
        """
        Draws projectile on the screen
        :return: None
        """
        if self.direction or self.penguin.enemy:
            rotated_image = pygame.transform.rotate(self.img, -90)
        else:
            rotated_image = pygame.transform.rotate(self.img, 90)
        win.blit(rotated_image, (self.x, self.y))

    def move(self):
        """
        Moves projectile on the screen
        :return: None
        """
        if self.direction or self.penguin.enemy:
            self.x -= (self.penguin.get_vel() + 15)
        else:
            self.x += self.penguin.get_vel() + 15

    def collide(self, penguin):
        """
        Checks if projectile collides with penguin
        :param penguin:
        :return: True if collided
        """
        penguin_mask = penguin.get_mask()
        projectile_mask = pygame.mask.from_surface(self.img)

        offset = (self.x - penguin.get_x(), self.y - penguin.get_y())
        return penguin_mask.overlap(projectile_mask, offset)
