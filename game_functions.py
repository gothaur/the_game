import pygame
import sys
from projectile import Projectile
from penguin import Enemy
from loot import Health, Ammo, Trap
import random


def check_keydown_events(event, settings, player, bullets, f_img, b_img):
    if event.key == pygame.K_RIGHT:
        player.move_right = True
    elif event.key == pygame.K_LEFT:
        player.move_left = True
    elif event.key == pygame.K_UP:
        player.move_up = True
    elif event.key == pygame.K_DOWN:
        player.move_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, player, bullets, f_img, b_img)


def check_keyup_events(event, player):
    if event.key == pygame.K_RIGHT:
        player.move_right = False
    if event.key == pygame.K_LEFT:
        player.move_left = False
    if event.key == pygame.K_UP:
        player.move_up = False
    if event.key == pygame.K_DOWN:
        player.move_down = False


def check_events(settings, player, bullets, f_img, b_img):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, player, bullets, f_img, b_img)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player)


def fire_bullet(settings, player, bullets, f_img, b_img):
    if player.has_ammo():
        bullets.add(Projectile(settings, player, f_img, b_img))
        player.ammo -= 1


def update_screen(settings, background, screen, player, enemies, bullets, loots):
    pass


def update_bullets(settings, bullets, enemies, player, loot_list, TRAP_IMG, HEALTH_IMG, GUN_IMG):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.x < 0 + bullet.width or bullet.x >= settings.screen_width - 2 * bullet.width:
            bullets.remove(bullet)

        if bullet.collide(player):
            player.lives -= 1
            bullets.remove(bullet)

        for enemy in enemies.copy():
            if bullet.collide(enemy):
                enemy.lives -= 1
                if not enemy.is_alive():
                    player.score += 1
                    if enemy.chance_to_drop(settings.chance_to_drop):
                        randomize_loot = [Trap(settings, enemy, settings.ground_speed, TRAP_IMG),
                                          Health(settings, enemy, settings.ground_speed, HEALTH_IMG),
                                          Ammo(settings, enemy, settings.ground_speed, GUN_IMG)]
                        ind = random.randint(0, 2)
                        loot_list.append(randomize_loot[ind])
                    bullets.remove(bullet)
                    enemies.remove(enemy)


def update_enemies(settings, enemies, bullets, reversed_penguin_images, bullet_image, reversed_bullet_image):
    if len(enemies) < 1:
        enemies.append(Enemy(settings, 1200, random.randint(530, 630), reversed_penguin_images))

    for enemy in enemies:
        enemy.update()
        enemy.fire(bullets, Projectile(settings, enemy, bullet_image, reversed_bullet_image))
        # we want different distance between next enemies
        distance = random.randint(600, 950)
        # we have to determinate last enemy to calculate distance between them
        max_dist = max(enemies, key=lambda x: x.x)
        last = max_dist.get_x()
        if len(enemies) < 6 and last < distance:
            enemies.append(Enemy(settings, 1200, random.randint(530, 630), reversed_penguin_images))


def update_loot(settings, loot_list, player):
    for loot in loot_list.copy():
        #  if loot goes out of the screen we want to remove it
        if loot.x < 0 or loot.x >= settings.screen_width:
            loot_list.remove(loot)

        if loot.collide(player):
            loot.buff(player)
            loot_list.remove(loot)

        loot.move()
