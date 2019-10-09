import pygame
import os


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

    def draw(self, win, list_of_objects, projectiles, loot_list):
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
            obj.draw()

        for projectile in projectiles:
            projectile.draw()

        for loot in loot_list:
            loot.draw()