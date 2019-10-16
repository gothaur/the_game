class Background:

    def __init__(self, bg_images, y=0):
        self.y = y
        self.bg_images = bg_images
        self.WIDTH = bg_images[0].get_width()
        self.HEIGHT = bg_images[0].get_height()
        self.TREE_HEIGHT = bg_images[0].get_height() - bg_images[2].get_height()
        self.ground_x1 = 0
        self.ground_x2 = self.WIDTH
        self.trees_x1 = 0
        self.trees_x2 = self.WIDTH
        self.dist_trees_x1 = 0
        self.dist_trees_x2 = self.WIDTH
        self.VEL_GROUND = 3
        self.VEL_TREES_AND_BUSHES = 2
        self.VEL_DISTANT_TREES = 1
        self. name = "Background"

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

    def draw(self, win, list_of_objects, projectiles, loot_list, player, my_font):
        win.blit(self.bg_images[0], (0, 0))
        win.blit(self.bg_images[1], (self.dist_trees_x1, 0))
        win.blit(self.bg_images[1], (self.dist_trees_x2, 0))
        win.blit(self.bg_images[2], (self.trees_x1, self.TREE_HEIGHT))
        win.blit(self.bg_images[2], (self.trees_x2, self.TREE_HEIGHT))
        win.blit(self.bg_images[3], (self.ground_x1, 90))
        win.blit(self.bg_images[3], (self.ground_x2, 90))

        # list of penguins must be in correct order to draw
        tmp = list_of_objects + loot_list
        tmp.sort(key=lambda x: x.y + x.get_height())
        for obj in tmp:
            obj.draw(win)

        for projectile in projectiles:
            projectile.draw(win)

        # for loot in loot_list:
        #     loot.draw(win)

        lives_text = f"""Lives: {player.lives}, Ammo: {player.ammo}"""
        text = my_font.render(lives_text, 1, (55, 55, 55))
        win.blit(text, (self.WIDTH - 10 - text.get_width(), 10))
