import pygame
import os
import random
from background import Background
from projectile import Projectile
from penguin import Penguin
from loot import Health, Ammo, Trap
pygame.font.init()


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
GUN_IMG = get_image("img/gun.png")
TRAP_IMG = get_image("img/trap.png")

# list of penguin images required to make movement animation
PENGUIN_IMGS = []
for i in range(0, 17):
    PENGUIN_IMGS.append(get_image(f"img/penguin/riffle/penguin{i}.png"))

RUNNING_IMG = get_image("img/penguin/run.png")
coord = [(x, y, 78, 73) for y in range(0, 147, 73) for x in range(0, 313, 78)]

STAT_FONT = pygame.font.SysFont('comicsans', 25)

HEIGHT = BG_IMGS[0].get_height()
WIDTH = BG_IMGS[0].get_width()

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player.has_ammo():
            bullets.append(Projectile(player, PROJECTILE_IMG))
            player.ammo -= 1

    add_enemy = False
    #  list of penguins to remove
    rem_p = []
    #  list of bullets to remove
    rem_b = []
    #  list of dropped items to remove
    rem_l = []

    pressed = pygame.key.get_pressed()
    player.move(pressed)

    for bullet in bullets:
        #  if bullet goes out of the screen we want to remove it
        if bullet.x < 0 or bullet.x >= WIDTH:
            rem_b.append(bullet)
        for elem in list_to_draw:
            if bullet.collide(elem):
                p = elem
                elem.lives -= 1
                if not elem.is_alive():
                    if p.chance_to_drop():
                        randomize_loot = [Trap(p, bg, TRAP_IMG), Health(p, bg, HEALTH_IMG), Ammo(p, bg, GUN_IMG)]
                        ind = random.randint(0, 2)
                        loot_list.append(randomize_loot[ind])
                    rem_p.append(elem)
                rem_b.append(bullet)

        bullet.move()

    for loot in loot_list:
        #  if loot goes out of the screen we want to remove it
        if loot.x < 0 or loot.x >= WIDTH:
            rem_l.append(loot)
        for penguin in list_to_draw:
            if loot.collide(penguin) and not penguin.enemy:
                loot.buff(penguin)
                rem_l.append(loot)

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

    for r in rem_l:
        try:
            loot_list.remove(r)
        except ValueError:
            # if an attempt to remove occurs there is no need to take action
            pass

    for elem in list_to_draw:
        elem.move(pressed)
        elem.fire(bullets, Projectile(elem, PROJECTILE_IMG))
        # we want different distance between next enemies
        distance = random.randint(600, 950)
        # we have to determinate last enemy to calculate distance between them
        max_dist = max(list_to_draw, key=lambda x: x.x)
        last = max_dist.get_x()
        if len(list_to_draw) < 6 and last < distance:
            list_to_draw.append(Penguin(1100, random.randint(520, 620), WIDTH,
                                        PENGUIN_IMGS, RUNNING_IMG, coord, enemy=True))

    bg.draw(screen, list_to_draw, bullets, loot_list, player, STAT_FONT)
    bg.move()
    pygame.display.flip()
    clock.tick(32)