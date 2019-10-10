import pygame


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
        self.x = penguin.x
        self.y = penguin.y
        self.vel = background.VEL_GROUND
        self.img = loot_img

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

    def buff(self, penguin):
        penguin.lives += 1
        print("Live added")


class Ammo(Loot):

    def __init__(self, penguin, background, loot_img):
        super().__init__(penguin, background, loot_img)


class Trap(Loot):

    def __init__(self, penguin, background, loot_img):
        super().__init__(penguin, background, loot_img)
