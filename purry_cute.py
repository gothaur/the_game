import pygame
import os
import random

_image_library = {}


def get_image(path):
    global _image_library
    image = _image_library.get(path)

    if image is None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image


BG_IMGS = [get_image("img/background.png"), get_image("img/distant_trees.png"),
           get_image("img/trees_and_bushes_1.png"), get_image("img/ground.png")]

PENGUIN_IMGS = []

for i in range(1, 17):
    PENGUIN_IMGS.append(get_image(f"img/penguin/Armature_run_{i}.png"))


class Background:
    VEL_GROUND = 3
    VEL_TREES_AND_BUSHES = 2
    VEL_DISTANT_TREES = 1
    WIDTH = BG_IMGS[0].get_width()
    IMG = BG_IMGS
    TREE_HEIGHT = IMG[0].get_height() - IMG[2].get_height()

    def __init__(self, y=0):
        self.y = y
        self.ground_x1 = 0
        self.ground_x2 = self.WIDTH
        self.trees_x1 = 0
        self.trees_x2 = self.WIDTH
        self.dist_trees_x1 = 0
        self.dist_trees_x2 = self.WIDTH

    def get_y(self):
        return self.y

    def move(self):
        self.ground_x1 -= self.VEL_GROUND
        self.ground_x2 -= self.VEL_GROUND
        self.trees_x1 -= self.VEL_TREES_AND_BUSHES
        self.trees_x2 -= self.VEL_TREES_AND_BUSHES
        self.dist_trees_x1 -= self.VEL_DISTANT_TREES
        self.dist_trees_x2 -= self.VEL_DISTANT_TREES

        if self.ground_x1 + self.WIDTH < 0:
            self.ground_x1 = self.ground_x2 + self.WIDTH

        if self.ground_x2 + self.WIDTH < 0:
            self.ground_x2 = self.ground_x1 + self.WIDTH

        if self.trees_x1 + self.WIDTH < 0:
            self.trees_x1 = self.trees_x2 + self.WIDTH

        if self.trees_x2 + self.WIDTH < 0:
            self.trees_x2 = self.trees_x1 + self.WIDTH

        if self.dist_trees_x1 + self.WIDTH < 0:
            self.dist_trees_x1 = self.dist_trees_x2 + self.WIDTH

        if self.dist_trees_x2 + self.WIDTH < 0:
            self.dist_trees_x2 = self.dist_trees_x1 + self.WIDTH

    def draw(self, win, list_of_objects):
        win.blit(self.IMG[0], (0, 0))
        win.blit(self.IMG[1], (self.dist_trees_x1, 0))
        win.blit(self.IMG[1], (self.dist_trees_x2, 0))
        win.blit(self.IMG[2], (self.trees_x1, self.TREE_HEIGHT))
        win.blit(self.IMG[2], (self.trees_x2, self.TREE_HEIGHT))
        win.blit(self.IMG[3], (self.ground_x1, 90))
        win.blit(self.IMG[3], (self.ground_x2, 90))

        list_of_objects.sort(key=lambda x: x.y)
        for obj in list_of_objects:
            obj.draw()


class Penguin:
    IMGS = PENGUIN_IMGS

    def __init__(self, x, y, lives=1, enemy=False):
        self.x = x
        self.y = y
        self.vel_forward = 5
        self.vel_backward = 3
        self.img_count = 0
        self.img = self.IMGS[0]
        self.WIDTH = self.img.get_width()
        self.HEIGHT = self.img.get_height()
        self.lives = lives
        self.moving_backward = False
        self.enemy = enemy

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def get_height(self):
        return self.img.get_height()

    def get_width(self):
        return self.WIDTH

    def is_alive(self):
        return self.lives > 0

    def move(self, key):
        if self.enemy:
            if self.x > 0:
                self.x -= 8
        else:
            self.moving_backward = False
            if key[pygame.K_UP] and self.y > 490:
                self.y -= 3
            if key[pygame.K_DOWN] and self.y < 620:
                self.y += 3
            if key[pygame.K_LEFT] and self.x > 0:
                self.x -= self.vel_backward
                self.moving_backward = True
            if key[pygame.K_RIGHT] and self.x < (1024 - self.WIDTH):
                self.x += self.vel_forward

    def draw(self):
        """
        Determinate direction and draw character on a screen
        :return:
        """
        if self.img_count > 15:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        if self.moving_backward or self.enemy:
            screen.blit(pygame.transform.flip(PENGUIN_IMGS[self.img_count], True, False), (self.x, self.y))
        else:
            screen.blit(PENGUIN_IMGS[self.img_count], (self.x, self.y))

        self.img_count += 1

    def get_mask(self):
        """

        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        print(pygame.mask.from_surface(self.img))
        return pygame.mask.from_surface(self.img)


pygame.init()
screen = pygame.display.set_mode((1024, 773))
done = False
bg = Background()
player = Penguin(100, 620, 2)
list_to_draw = [player, Penguin(1200, 620, enemy=True)]
clock = pygame.time.Clock()

while not done and player.is_alive():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    add_enemy = False
    rem = []
    pressed = pygame.key.get_pressed()
    player.move(pressed)

    for i in range(len(list_to_draw)):
        list_to_draw[i].move(pressed)
        distance = random.randint(600, 950) - random.randint(0, 100)
        if len(list_to_draw) < 6 and list_to_draw[-1].get_x() < distance:
            list_to_draw.append(Penguin(1100, random.randint(520, 620), enemy=True))

    bg.draw(screen, list_to_draw)
    bg.move()
    pygame.display.flip()
    clock.tick(32)
