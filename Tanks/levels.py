import pygame
from settings import *
from camera import CameraGroup
from base_player import Player
from random import randint


class Level:
    def __init__(self):

        # get the display surface
        self.window = pygame.display.get_surface()
        self.game_paused = False

        # sprite group setup
        self.visible_sprites = CameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # players
        self.player = Player(self.visible_sprites, "../images/panzer.png", 200, 200, 50, 50, 6, 6, True)

        for _ in range(100):
            Player(self.visible_sprites, "../images/enemy.png", randint(0, 2400), randint(0, 1400), 50, 50, 3, 3)

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
