import pygame
import os
import random
from background import Background
from penguin import Player, Enemy
from settings import Settings
import game_functions as gf
from pygame.sprite import Group

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

done = False
bg = Background(settings, BG_IMGS, HEALTH_IMG, PROJECTILE_IMG)
player = Player(settings, 100, 620, F_PENGUIN_IMGS, B_PENGUIN_IMGS)
enemies = [Enemy(settings, 1200, random.randint(530, 630), B_PENGUIN_IMGS)]

loot_list = []
bullets = Group()
clock = pygame.time.Clock()

while not done and player.is_alive():
    gf.check_events(settings, player, bullets, F_PROJECTILE_IMG, B_PROJECTILE_IMG)
    gf.update_bullets(settings, bullets, enemies, player, loot_list, TRAP_IMG, HEALTH_IMG, GUN_IMG)
    player.update()
    gf.update_loot(settings, loot_list, player)
    gf.update_enemies(settings, enemies, bullets, B_PENGUIN_IMGS, F_PROJECTILE_IMG, B_PROJECTILE_IMG)
    bg.draw(screen, enemies, bullets, loot_list, player, STAT_FONT)
    bg.move()
    pygame.display.flip()
    clock.tick(settings.fps)
