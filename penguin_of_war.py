import pygame
import os
import random


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

# list of penguin images required to make movement animation
PENGUIN_IMGS = []
for i in range(1, 17):
    PENGUIN_IMGS.append(get_image(f"img/penguin/Armature_run_{i}.png"))

RUNNING_IMG = get_image("img/penguin/run.png")
coord = [(x, y, 78, 73) for y in range(0, 147, 73) for x in range(0, 313, 78)]

HEIGHT = BG_IMGS[0].get_height()
WIDTH = BG_IMGS[0].get_width()


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

    def move(self, player):
        if player.is_moving:
            if player.moving_backward:
                self.ground_x1 -= (self.VEL_GROUND - player.get_vel())
                self.ground_x2 -= (self.VEL_GROUND - player.get_vel())
                self.trees_x1 -= self.VEL_TREES_AND_BUSHES - player.get_vel()
                self.trees_x2 -= self.VEL_TREES_AND_BUSHES - player.get_vel()
                self.dist_trees_x1 -= self.VEL_DISTANT_TREES - player.get_vel()
                self.dist_trees_x2 -= self.VEL_DISTANT_TREES - player.get_vel()
            else:
                self.ground_x1 -= (self.VEL_GROUND + player.get_vel())
                self.ground_x2 -= (self.VEL_GROUND + player.get_vel())
                self.trees_x1 -= self.VEL_TREES_AND_BUSHES + player.get_vel()
                self.trees_x2 -= self.VEL_TREES_AND_BUSHES + player.get_vel()
                self.dist_trees_x1 -= self.VEL_DISTANT_TREES + player.get_vel()
                self.dist_trees_x2 -= self.VEL_DISTANT_TREES + player.get_vel()
        else:
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

    def draw(self, win, list_of_objects, projectiles):
        win.blit(self.IMG[0], (0, 0))
        win.blit(self.IMG[1], (self.dist_trees_x1, 0))
        win.blit(self.IMG[1], (self.dist_trees_x2, 0))
        win.blit(self.IMG[2], (self.trees_x1, self.TREE_HEIGHT))
        win.blit(self.IMG[2], (self.trees_x2, self.TREE_HEIGHT))
        win.blit(self.IMG[3], (self.ground_x1, 90))
        win.blit(self.IMG[3], (self.ground_x2, 90))

        # list of penguins must be in correct order to draw
        list_of_objects.sort(key=lambda x: x.y)
        for obj in list_of_objects:
            obj.draw_1()

        for projectile in projectiles:
            projectile.draw()


class Penguin:
    IMGS = PENGUIN_IMGS
    RUN = RUNNING_IMG

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
        self.is_moving = False

    def get_vel(self):
        return self.vel_forward

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

    def fire(self, bullets):
        if self.enemy and random.randint(1, 100) < 11:
            bullets.append(Projectile(self))
            print(f"fireing!{Projectile(self)}")
            # return Projectile(self)

    def move(self, key):
        if self.enemy:
            if self.x > 0:
                self.x -= 8
        else:
            self.moving_backward = False
            self.is_moving = False
            if key[pygame.K_UP] and self.y > 595 - self.HEIGHT:
                self.y -= 3
            if key[pygame.K_DOWN] and self.y < 620:
                self.y += 3
            if key[pygame.K_LEFT] and self.x > 0:
                self.x -= self.vel_backward
                self.moving_backward = True
                self.is_moving = True
            if key[pygame.K_RIGHT] and self.x < (1024 - self.WIDTH):
                self.is_moving = True
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

    def draw_1(self):
        if self.img_count > 14:
            self.img_count = 0

        # we want to know if character moves backward to reverse image
        if self.moving_backward or self.enemy:
            screen.blit(pygame.transform.flip(RUNNING_IMG, True, False), (self.x, self.y), coord[-self.img_count])
        else:
            screen.blit(RUNNING_IMG, (self.x, self.y), coord[self.img_count])

        self.img_count += 1

    def get_mask(self):
        """
        :return: tuple of coordinates of object edges needed to determinate if hit
        """
        return pygame.mask.from_surface(self.img)


class Projectile:
    IMG = PROJECTILE_IMG

    def __init__(self, penguin):
        """
        :type penguin: object
        """
        self.direction = penguin.moving_backward
        if self.direction:
            self.x = penguin.get_x() - 10
        else:
            self.x = penguin.get_x() + penguin.get_height()
        self.y = int(penguin.get_y() + penguin.get_width() / 2)
        self.penguin = penguin

    def draw(self):
        rotated_image = pygame.transform.rotate(self.IMG, 90)
        screen.blit(rotated_image, (self.x, self.y))

    def move(self):
        if self.direction:
            self.x -= (self.penguin.get_vel() + 15)
        else:
            self.x += self.penguin.get_vel() + 15

    def collide(self, penguin):
        penguin_mask = penguin.get_mask()
        projectile_mask = pygame.mask.from_surface(self.IMG)

        offset = (self.x - penguin.get_x(), self.y - penguin.get_y())
        return penguin_mask.overlap(projectile_mask, offset)


pygame.init()
screen = pygame.display.set_mode((1024, 773))
done = False
bg = Background()
player = Penguin(100, 620, 2)
list_to_draw = [player, Penguin(1200, 620, enemy=True)]
bullets = []
clock = pygame.time.Clock()

while not done and player.is_alive():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullets.append(Projectile(player))

    add_enemy = False
    rem_p = []
    rem_b = []

    pressed = pygame.key.get_pressed()
    player.move(pressed)

    for bullet in bullets:
        if bullet.x >= WIDTH:
            rem_b.append(bullet)
        for i in range(len(list_to_draw)):
            if bullet.collide(list_to_draw[i]):
                list_to_draw[i].lives -= 1
                if not list_to_draw[i].is_alive():
                    rem_p.append(list_to_draw[i])
                rem_b.append(bullet)

        bullet.move()

    for r in rem_p:
        try:
            list_to_draw.remove(r)
        except Exception:
            print("Attempt to remove non existing penguin")

    for r in rem_b:
        try:
            bullets.remove(r)
        except Exception:
            print("Attempt to remove non existing bullet")

    for i in range(len(list_to_draw)):
        list_to_draw[i].move(pressed)
        list_to_draw[i].fire(bullets)
        distance = random.randint(600, 950) - random.randint(0, 100)
        if len(list_to_draw) < 6 and list_to_draw[-1].get_x() < distance:
            list_to_draw.append(Penguin(1100, random.randint(520, 620), enemy=True))

    bg.draw(screen, list_to_draw, bullets)
    bg.move(player)
    pygame.display.flip()
    clock.tick(32)
