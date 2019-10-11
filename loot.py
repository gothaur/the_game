import pygame
import random


class Loot:
    """
    Loot object witch can buff our penguin
    """

    def __init__(self, penguin, background, loot_img):
        """

        :param penguin: penguin witch dropped item
        :param background: background [needed to determinate position on the screen
        :param loot_img: image of dropped item
        """
        self.x = penguin.x + int(penguin.get_width() / 2)
        self.y = penguin.y + int(penguin.get_height() / 2)
        self.vel = background.VEL_GROUND
        self.img = loot_img
        self.name = ''

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

    def buff(self):
        pass


class Health(Loot):

    def __init__(self, penguin, background, loot_img):
        super().__init__(penguin, background, loot_img)
        self.name = 'Health'

    def buff(self, penguin):
        penguin.lives += 1


class Ammo(Loot):

    def __init__(self, penguin, background, loot_img):
        super().__init__(penguin, background, loot_img)
        self.name = 'Ammo'

    def buff(self, penguin):
        penguin.ammo += 10


class Trap(Loot):

    def __init__(self, penguin, background, loot_img):
        super().__init__(penguin, background, loot_img)
        self.name = 'Trap'

    def buff(self, penguin):
        randomize = random.randint(0, 100)
        if 0 < randomize < 15:
            penguin.lives += 1
        elif 16 < randomize < 90:
            penguin.ammo += 10
        else:
            penguin.lives -= 1
