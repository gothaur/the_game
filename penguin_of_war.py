import pygame
import os
import random
from background import Background
from projectile import Projectile
from penguin import Penguin
from loot import Loot


def get_image(path):
    """
    Changes slash or backslash depends of the system you uses
    :param path:
    :return image with correct path:
    """
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    return pygame.image.load(canonicalized_path)


# list of images to draw a background
BG_IMGS = [get_image("img/background.png"), get_image("img/distant_trees.png"),
           get_image("img/trees_and_bushes_1.png"), get_image("img/ground.png")]

PROJECTILE_IMG = get_image("img/projectile.png")
HEALTH_IMG = get_image("img/health.png")

# list of penguin images required to make movement animation
PENGUIN_IMGS = []
for i in range(1, 17):
    PENGUIN_IMGS.append(get_image(f"img/penguin/Armature_run_{i}.png"))

RUNNING_IMG = get_image("img/penguin/run.png")
coord = [(x, y, 78, 73) for y in range(0, 147, 73) for x in range(0, 313, 78)]

HEIGHT = BG_IMGS[0].get_height()
WIDTH = BG_IMGS[0].get_width()


# class Loot:
#     """
#     Loot object witch can buff our penguin
#     """
#
#     def __init__(self, p, bg):
#         """
#
#         :param p: penguin witch dropped item
#         :param bg: background [needed to determinate position on the screen
#         """
#         self.x = p.x
#         self.y = p.y
#         self.vel = bg.VEL_GROUND
#         self.img = HEALTH_IMG
#
#     def move(self):
#         self.x -= self.vel
#
#     def draw(self, win):
#         win.blit(self.img, (self.x, self.y))
#
#     def collide(self, penguin):
#         """
#         Checks if projectile collides with penguin
#         :param penguin:
#         :return: True if collided
#         """
#         penguin_mask = penguin.get_mask()
#         loot_mask = pygame.mask.from_surface(self.img)
#
#         offset = (self.x - penguin.get_x(), self.y - penguin.get_y())
#         return penguin_mask.overlap(loot_mask, offset)
#

pygame.init()
screen = pygame.display.set_mode((1024, 773))
done = False
bg = Background(BG_IMGS)
player = Penguin(100, 620, WIDTH, PENGUIN_IMGS, RUNNING_IMG, coord, 2)
list_to_draw = [player, Penguin(1200, 620, WIDTH, PENGUIN_IMGS, RUNNING_IMG, coord, enemy=True)]
loot_list = []
bullets = []
clock = pygame.time.Clock()

while not done and player.is_alive():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Projectile(player, PROJECTILE_IMG))

    add_enemy = False
    rem_p = []
    rem_b = []

    pressed = pygame.key.get_pressed()
    player.move(pressed)

    for bullet in bullets:
        if 0 > bullet.x >= WIDTH:
            rem_b.append(bullet)
        for i in range(len(list_to_draw)):
            if bullet.collide(list_to_draw[i]):
                p = list_to_draw[i]
                list_to_draw[i].lives -= 1
                if not list_to_draw[i].is_alive():
                    if p.chance_to_drop():
                        print('upuscilem cos')
                        loot_list.append(Loot(p, bg, HEALTH_IMG))
                    rem_p.append(list_to_draw[i])
                rem_b.append(bullet)

        bullet.move()

    for loot in loot_list:
        loot.move()

    for r in rem_p:
        try:
            list_to_draw.remove(r)
        except ValueError:
            # if an attempt to remove occurs there is no need to take action
            pass

    for r in rem_b:
        try:
            bullets.remove(r)
        except ValueError:
            # if an attempt to remove occurs there is no need to take action
            pass

    for i in range(len(list_to_draw)):
        list_to_draw[i].move(pressed)
        list_to_draw[i].fire(bullets, Projectile(list_to_draw[i], PROJECTILE_IMG))
        # we want different distance between next enemies
        distance = random.randint(600, 950)
        # we have to determinate last enemy to calculate distance between them
        max_dist = max(list_to_draw, key=lambda x: x.x)
        last = max_dist.get_x()
        if len(list_to_draw) < 6 and last < distance:
            list_to_draw.append(Penguin(1100, random.randint(520, 620), WIDTH, PENGUIN_IMGS, RUNNING_IMG, coord, enemy=True))

    bg.draw(screen, list_to_draw, bullets, loot_list)
    bg.move()
    pygame.display.flip()
    clock.tick(32)
