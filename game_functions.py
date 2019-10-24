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
    elif event.key == pygame.K_F4 and pygame.KMOD_ALT:
        sys.exit()


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


def update_bullets(settings, bullets, enemies, player, bullet_image, reversed_bullet_image, loot_list, loot_images):

    for bullet in bullets.copy():
        if bullet.x < 0 + bullet.width or bullet.x >= settings.screen_width - 2 * bullet.width:
            bullets.remove(bullet)

        if bullet.collide(player):
            player.lives -= 1
            bullets.remove(bullet)

        for enemy in enemies.copy():
            if bullet.collide(enemy):
                enemy.lives -= 1
                bullets.remove(bullet)
                try_to_drop_loop(settings, enemy, loot_list, loot_images)
            if len(bullets) < 11:
                enemy.fire(bullets, Projectile(settings, enemy, bullet_image, reversed_bullet_image))

        bullet.move()


def try_to_drop_loop(settings, enemy, loot_list, loot_images):
    if enemy.chance_to_drop:
        roll = random.randint(0, 100)
        if roll <= settings.chance_to_drop_present:
            loot_list.append(Trap(settings, enemy, loot_images[0]))
        elif roll <= settings.chance_to_drop_health:
            loot_list.append(Health(settings, enemy, loot_images[1]))
        else:
            loot_list.append(Ammo(settings, enemy, loot_images[2]))


def update_enemies(settings, enemies, reversed_penguin_images):
    if len(enemies) < 1:
        enemies.append(Enemy(settings, 1200, random.randint(530, 630), reversed_penguin_images))

    for enemy in enemies.copy():
        if enemy.is_dead():
            enemies.remove(enemy)
            continue
        enemy.update()
        # we want different distance between next enemies
        distance = random.randint(850, 950)
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
