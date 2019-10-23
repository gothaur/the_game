import pygame
import os
import random
from background import Background
from projectile import Projectile
from penguin import Penguin
from settings import Settings
from loot import Health, Ammo, Trap
import game_functions as gf

pygame.font.init()
pygame.init()
settings = Settings()
my_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
screen = pygame.display.set_mode(settings.get_screen_size(), my_flags)


def get_image(path):
    """
    Changes slash or backslash depends of the system you uses
    :param path:
    :return image with correct path:
    """
    canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
    return pygame.image.load(canonicalized_path).convert_alpha()


#####################################################################################
# list of images to draw a background
BG_IMGS = [get_image("img/background.png"), get_image("img/distant_trees.png"),
           get_image("img/trees_and_bushes_1.png"), get_image("img/ground.png")]

#  images to draw as pictogram to inform player of his bullet status
PROJECTILE_IMG = get_image("img/projectile.png")
#  rotated image to draw when firing moving forward
F_PROJECTILE_IMG = pygame.transform.rotate(PROJECTILE_IMG, 90)
#  rotated image to draw when firing moving backward
B_PROJECTILE_IMG = pygame.transform.rotate(PROJECTILE_IMG, -90)
#  health image
HEALTH_IMG = get_image("img/health.png")
GUN_IMG = get_image("img/gun.png")
TRAP_IMG = get_image("img/trap.png")
#####################################################################################
# list of penguin images required to make forward movement animation
F_PENGUIN_IMGS = []
for i in range(0, 17):
    # PENGUIN_IMGS.append(get_image(f"img/penguin/riffle/penguin{i}.png"))
    path = "img/penguin/riffle/penguin" + str(i) + ".png"
    F_PENGUIN_IMGS.append(get_image(path))

# list of penguin images required to make backward movement animation
B_PENGUIN_IMGS = []
for img in F_PENGUIN_IMGS:
    B_PENGUIN_IMGS.append(pygame.transform.flip(img, True, False))

STAT_FONT = pygame.font.SysFont('comicsans', 35)

HEIGHT = BG_IMGS[0].get_height()
WIDTH = BG_IMGS[0].get_width()

# pygame.init()
# my_flags = pygame.DOUBLEBUF | pygame.HWSURFACE
# screen = pygame.display.set_mode((1024, 773), my_flags)
done = False
bg = Background(BG_IMGS, HEALTH_IMG, PROJECTILE_IMG)
player = Penguin(settings, 100, 620, WIDTH, F_PENGUIN_IMGS, B_PENGUIN_IMGS, 2)
list_to_draw = [player, Penguin(settings, 1200, random.randint(530, 630), WIDTH,
                                F_PENGUIN_IMGS, B_PENGUIN_IMGS, enemy=True)]
loot_list = []
bullets = []
clock = pygame.time.Clock()

while not done and player.is_alive():
    gf.check_events(settings, player, bullets, F_PROJECTILE_IMG, B_PROJECTILE_IMG)

    for bullet in bullets:
        #  if bullet goes out of the screen we want to remove it
        if bullet.x < 0 + bullet.width or bullet.x >= WIDTH - 2 * bullet.width:
            bullets.remove(bullet)
        for elem in list_to_draw:
            if bullet.collide(elem):
                p = elem
                elem.lives -= 1
                if not elem.is_alive():
                    player.score += 1
                    if p.chance_to_drop(settings.chance_to_drop):
                        randomize_loot = [Trap(p, bg, TRAP_IMG), Health(p, bg, HEALTH_IMG), Ammo(p, bg, GUN_IMG)]
                        ind = random.randint(0, 2)
                        loot_list.append(randomize_loot[ind])
                    list_to_draw.remove(elem)
                try:
                    bullets.remove(bullet)
                except ValueError:
                    pass

        bullet.move()

    for loot in loot_list:
        #  if loot goes out of the screen we want to remove it
        if loot.x < 0 or loot.x >= WIDTH:
            loot_list.remove(loot)
        for penguin in list_to_draw:
            if loot.collide(penguin) and not penguin.enemy:
                loot.buff(penguin)
                try:
                    loot_list.remove(loot)
                except ValueError:
                    pass

        loot.move()

    for elem in list_to_draw:
        elem.update_player()
        elem.update_enemy()
        elem.fire(bullets, Projectile(settings, elem, F_PROJECTILE_IMG, B_PROJECTILE_IMG))
        # we want different distance between next enemies
        distance = random.randint(600, 950)
        # we have to determinate last enemy to calculate distance between them
        max_dist = max(list_to_draw, key=lambda x: x.x)
        last = max_dist.get_x()
        if len(list_to_draw) < 6 and last < distance:
            list_to_draw.append(Penguin(settings, 1100, random.randint(530, 630), WIDTH,
                                        F_PENGUIN_IMGS, B_PENGUIN_IMGS, enemy=True))

    bg.draw(screen, list_to_draw, bullets, loot_list, player, STAT_FONT)
    bg.move()
    pygame.display.flip()
    clock.tick(settings.fps)
