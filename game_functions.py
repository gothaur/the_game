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


def fire_bullet(settings, player, player_bullets, f_img, b_img):
    if player.has_ammo() and len(player_bullets) < settings.max_player_bullets:
        player_bullets.add(Projectile(settings, player, f_img, b_img))
        player.ammo -= 1


def take_shot(settings, enemy_bullets, enemies, player, bullet_image, reversed_bullet_image):
    for enemy in enemies:
        enemy_y = enemy.get_y() + enemy.get_height() / 2
        if len(enemy_bullets) < settings.max_enemy_bullets \
                and player.get_y() + player.get_height() >= enemy_y >= player.get_y() \
                and player.get_x() < enemy.get_x():
            enemy.fire(enemy_bullets, Projectile(settings, enemy, bullet_image, reversed_bullet_image))


def update_enemy_bullets(enemy_bullets, player):
    for bullet in enemy_bullets.copy():
        if bullet.x < 0 + bullet.width:
            enemy_bullets.remove(bullet)

        if bullet.collide(player):
            player.lives -= 1
            enemy_bullets.remove(bullet)

        bullet.move()


def update_player_bullets(settings, player_bullets, enemies, loot_list, loot_images):

    for bullet in player_bullets.copy():
        if bullet.x < 0 + bullet.width or bullet.x >= settings.screen_width - 2 * bullet.width:
            player_bullets.remove(bullet)

        for enemy in enemies.copy():

            in_range(settings, bullet, enemy)

            if bullet.collide(enemy):
                enemy.lives -= 1
                player_bullets.remove(bullet)
                try_to_drop_loop(settings, enemy, loot_list, loot_images)

        bullet.move()


def in_range(settings, bullet, enemy):

    bullet_y = bullet.y + bullet.width / 2
    enemy_y = enemy.y + enemy.get_height() / 2

    if enemy.get_x() > bullet.x and enemy.get_y() - bullet.y <= settings.enemy_field_of_view:
        if enemy.y <= bullet_y <= enemy_y:
            enemy.y += 10
        elif enemy_y < bullet.y <= enemy.y + enemy.get_height():
            enemy.y -= 10


def try_to_drop_loop(settings, enemy, loot_list, loot_images):
    if enemy.chance_to_drop:
        roll = random.randint(0, 100)
        if roll <= settings.chance_to_drop_present:
            loot_list.append(Trap(settings, enemy, loot_images[0]))
        elif roll <= settings.chance_to_drop_health + settings.chance_to_drop_present:
            loot_list.append(Health(settings, enemy, loot_images[1]))
        else:
            loot_list.append(Ammo(settings, enemy, loot_images[2]))


def update_enemies(settings, enemies, reversed_penguin_images):
    if len(enemies) < 1:
        enemies.append(Enemy(settings, 1200, random.randint(530, 630), reversed_penguin_images))

    for x, enemy in enumerate(enemies.copy()):
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
