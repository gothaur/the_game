import pygame
import os
import random
from background import Background


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


class Penguin:
    RUN = RUNNING_IMG

    def __init__(self, x, y, lives=1, enemy=False):
        self.x = x
        self.y = y
        self.vel_forward = 5
        self.vel_backward = 3
        self.img_count = 0
        self.img = PENGUIN_IMGS[0]
        self.WIDTH = 78
        self.HEIGHT = 73
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
        return self.HEIGHT

    def get_width(self):
        return self.WIDTH

    def is_alive(self):
        return self.lives > 0

    def fire(self, bullet_list):
        if self.enemy and self.x < WIDTH and random.randint(1, 100) < 5:
            bullet_list.append(Projectile(self))

    def chance_to_drop(self):
        return random.randint(1, 100) < 15

    def move(self, key):
        if self.enemy:
            if self.x > 0:
                self.x -= 8
        else:
            self.moving_backward = False
            self.is_moving = False
            if key[pygame.K_UP] and self.y > 595 - self.HEIGHT:
                self.y -= 5
            if key[pygame.K_DOWN] and self.y < 620:
                self.y += 5
            if key[pygame.K_LEFT] and self.x > 0:
                self.x -= self.vel_backward
                self.moving_backward = True
                self.is_moving = True
            if key[pygame.K_RIGHT] and self.x < (1024 - self.WIDTH):
                self.is_moving = True
                self.x += self.vel_forward

    def draw(self):
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

    def __init__(self, penguin, loot=False):
        """

        :param penguin: penguin who fired or dropped object
        :param loot: type bool determinate if can buff player
        """
        self.direction = penguin.moving_backward
        if self.direction or penguin.enemy:
            self.x = penguin.x - 10
        else:
            self.x = penguin.x + penguin.get_height()
        self.y = int(penguin.y + penguin.get_width() / 2)
        self.penguin = penguin
        self.loot = loot

    def draw(self):
        """
        Draws projectile on the screen
        :return: None
        """
        if self.direction or self.penguin.enemy:
            rotated_image = pygame.transform.rotate(self.IMG, -90)
        else:
            rotated_image = pygame.transform.rotate(self.IMG, 90)
        screen.blit(rotated_image, (self.x, self.y))

    def move(self):
        """
        Moves projectile on the screen
        :return: None
        """
        if self.direction or self.penguin.enemy:
            self.x -= (self.penguin.get_vel() + 15)
        else:
            self.x += self.penguin.get_vel() + 15

    def collide(self, penguin):
        """
        Checks if projectile collides with penguin
        :param penguin:
        :return: True if collided
        """
        penguin_mask = penguin.get_mask()
        projectile_mask = pygame.mask.from_surface(self.IMG)

        offset = (self.x - penguin.get_x(), self.y - penguin.get_y())
        return penguin_mask.overlap(projectile_mask, offset)


class Loot:
    """
    Loot object witch can buff our penguin
    """

    def __init__(self, p, bg):
        """

        :param p: penguin witch dropped item
        :param bg: background [needed to determinate position on the screen
        """
        self.x = p.x
        self.y = p.y
        self.vel = bg.VEL_GROUND
        self.img = HEALTH_IMG

    def move(self):
        self.x -= self.vel

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

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


pygame.init()
screen = pygame.display.set_mode((1024, 773))
done = False
bg = Background(BG_IMGS)
player = Penguin(100, 620, 2)
list_to_draw = [player, Penguin(1200, 620, enemy=True)]
loot_list = []
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
        if 0 > bullet.x >= WIDTH:
            rem_b.append(bullet)
        for i in range(len(list_to_draw)):
            if bullet.collide(list_to_draw[i]):
                p = list_to_draw[i]
                list_to_draw[i].lives -= 1
                if not list_to_draw[i].is_alive():
                    if p.chance_to_drop():
                        print('upuscilem cos')
                        loot_list.append(Loot(p, bg))
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
        list_to_draw[i].fire(bullets)
        # we want different distance between next enemies
        distance = random.randint(600, 950)
        # we have to determinate last enemy to calculate distance between them
        max_dist = max(list_to_draw, key=lambda x: x.x)
        last = max_dist.get_x()
        if len(list_to_draw) < 6 and last < distance:
            list_to_draw.append(Penguin(1100, random.randint(520, 620), enemy=True))

    bg.draw(screen, list_to_draw, bullets, loot_list)
    bg.move()
    pygame.display.flip()
    clock.tick(32)
