import pygame
import os

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
           get_image("img/trees_and_bushes.png"), get_image("img/ground.png")]

PENGUIN_IMGS = []

for i in range(1, 17):
    PENGUIN_IMGS.append(get_image(f"img/penguin/Armature_run_{i}.png"))


class Background:
    VEL_GROUND = 3
    VEL_TREES_AND_BUSHES = 2
    VEL_DISTANT_TREES = 1
    WIDTH = BG_IMGS[0].get_width()
    print(f"szerokosc: {WIDTH}")
    IMG = BG_IMGS

    def __init__(self, y=0):
        self.y = y
        self.ground_x1 = 0
        self.ground_x2 = self.WIDTH
        self.trees_x1 = 0
        self.trees_x2 = self.WIDTH
        self.dist_trees_x1 = 0
        self.dist_trees_x2 = self.WIDTH

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

    def draw(self, win):
        win.blit(self.IMG[1], (self.dist_trees_x1, 0))
        win.blit(self.IMG[1], (self.dist_trees_x2, 0))
        win.blit(self.IMG[2], (self.trees_x1, 0))
        win.blit(self.IMG[2], (self.trees_x2, 0))
        win.blit(self.IMG[3], (self.ground_x1, 90))
        win.blit(self.IMG[3], (self.ground_x2, 90))


class Penguin:
    IMGS = PENGUIN_IMGS

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_forward = 5
        self.vel_backward = 3
        self.img_count = 0
        self.img = self.IMGS[0]

    def move_forward(self):
        self.x += self.vel_forward

    def move_backward(self):
        self.y -= self.vel_backward

    def move(self, key):
        if key[pygame.K_UP]:
            self.y -= 3
        if key[pygame.K_DOWN]:
            if self.y < 620:
                self.y += 3
        if key[pygame.K_LEFT]:
            self.x -= self.vel_backward
        if key[pygame.K_RIGHT]:
            self.x += self.vel_forward

    def draw(self):
        if self.img_count > 15:
            self.img_count = 0

        screen.blit(PENGUIN_IMGS[self.img_count], (self.x, self.y))
        self.img_count += 1

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


pygame.init()
screen = pygame.display.set_mode((1024, 773))
done = False
bg = Background()
penguin = Penguin(100, 620)
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    penguin.move(pressed)
    screen.blit(get_image("img/background.png"), (0, 0))
    bg.draw(screen)
    bg.move()
    penguin.draw()
    pygame.display.flip()
    clock.tick(30)
