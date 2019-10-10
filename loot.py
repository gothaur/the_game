import pygame


class Loot:
    """
    Loot object witch can buff our penguin
    """

    def __init__(self, p, bg, img):
        """

        :param p: penguin witch dropped item
        :param bg: background [needed to determinate position on the screen
        :param img: image of dropped item
        """
        self.x = p.x
        self.y = p.y
        self.vel = bg.VEL_GROUND
        self.img = img

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def collide(self, penguin):
        """
        Checks if projectile collides with penguin
        :param penguin:
        :return: True if collided
        """
        penguin_mask = penguin.get_mask()
        loot_mask = pygame.mask.from_surface(self.img)

        offset = (self.x - penguin.get_x(), self.y - penguin.get_y())
        return penguin_mask.overlap(loot_mask, offset)
