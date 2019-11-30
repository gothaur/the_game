class Background:

    def __init__(self, settings, bg_images, health_img, bullet_img, y=0):
        self.y = y
        self.bg_images = bg_images
        self.health_img = health_img
        self.bullet_img = bullet_img
        self.WIDTH = bg_images[0].get_width()
        self.HEIGHT = bg_images[0].get_height()
        self.TREE_HEIGHT = bg_images[0].get_height() - bg_images[2].get_height()
        self.ground_x1 = 0
        self.ground_x2 = self.WIDTH
        self.trees_x1 = 0
        self.trees_x2 = self.WIDTH
        self.dist_trees_x1 = 0
        self.dist_trees_x2 = self.WIDTH
        self.settings = settings
        self.VEL_TREES_AND_BUSHES = 2
        self.VEL_DISTANT_TREES = 1
        self. name = "Background"

    def get_y(self):
        return self.y

    def move(self):
        self.ground_x1 -= self.settings.ground_speed
        self.ground_x2 -= self.settings.ground_speed
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

    def draw(self,settings, win, enemies, player_projectiles, enemy_projectiles, loot_list, player, my_font):
        win.blit(self.bg_images[0], (0, 0))
        win.blit(self.bg_images[1], (self.dist_trees_x1, 0))
        win.blit(self.bg_images[1], (self.dist_trees_x2, 0))
        win.blit(self.bg_images[2], (self.trees_x1, self.TREE_HEIGHT))
        win.blit(self.bg_images[2], (self.trees_x2, self.TREE_HEIGHT))
        win.blit(self.bg_images[3], (self.ground_x1, self.settings.ground_bottom))
        win.blit(self.bg_images[3], (self.ground_x2, self.settings.ground_bottom))

        # list of penguins must be in correct order to draw
        tmp = enemies + loot_list
        tmp.append(player)
        tmp.sort(key=lambda x: x.y + x.get_height())
        for obj in tmp:
            obj.draw(win)

        for projectile in player_projectiles:
            projectile.draw(win)

        for projectile in enemy_projectiles:
            projectile.draw(win)

        for i in range(0, player.lives):
            win.blit(self.health_img, (10 * i, 10))

        for i in range(0, player.ammo):
            win.blit(self.bullet_img, (self.WIDTH - 5 * i - self.bullet_img.get_width(), 10))
            if i >= 25:
                break

        score_text = my_font.render(f'SCORE: {settings.score}', False, (0, 0, 0))
        win.blit(score_text, (int(self.WIDTH / 2 - score_text.get_width() / 2), 10))
