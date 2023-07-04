import pygame
from settings import *


class GameSprite(pygame.sprite.Sprite):
    def __init__(self):
        super.__init__(self)
        # self.rect = pygame.rect.Rect(BLOCKSIZE, BLOCKSIZE)





class GameSpriteImage(GameSprite):
    def __init__(self):
        super.__init__(self)
