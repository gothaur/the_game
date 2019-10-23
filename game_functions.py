import pygame
import sys
from projectile import Projectile


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
        bullets.append(Projectile(settings, player, f_img, b_img))
        player.ammo -= 1
