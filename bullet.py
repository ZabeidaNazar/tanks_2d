import pygame
from settings import *
from game_map import *

class Bullet:
    def __init__(self, tank, filename, speed):
        self.tank = tank
        self.image = pygame.transform.scale(pygame.image.load(filename).convert_alpha(), (BLOCKSIZE // 3, BLOCKSIZE // 3))
        self.rect = self.image.get_rect()
        self.rect.x = tank.rect.x + tank.rect.width // 2 - self.rect.width // 2
        self.rect.y = tank.rect.y + tank.rect.height // 2 - self.rect.height // 2
        # self.rect.x = tank.rect.x
        # self.rect.y = tank.rect.y

        self.speed = speed

        if tank.angle == 0:
            self.speed_x = 0
            self.speed_y = -speed
        elif tank.angle == 90:
            self.speed_x = -speed
            self.speed_y = 0
        elif tank.angle == 270:
            self.speed_x = speed
            self.speed_y = 0
        elif tank.angle == 180:
            self.speed_x = 0
            self.speed_y = speed

    # def __str__(self):
    #     return 

    def fight():
        pass

    def check_collide(self):
        for block in self.tank.game.blocks:
            if self.rect.colliderect(block):
                if self in self.tank.bullets:
                    self.tank.bullets.remove(self)
                if block.type_block == 1:
                    self.tank.game.blocks.remove(block)
                    game_map[block.y][block.x] = 0
                


    def draw(self):
        self.tank.game.main_screen.blit(self.image, (self.rect.x, self.rect.y))#    ; pygame.draw.rect(self.tank.game.main_screen, (255, 0, 0), self.rect, 1)
        self.rect.x += self.speed_x; self.rect.y += self.speed_y
        self.check_collide()



    def check_collide_count(self):
        for block in self.tank.game.blocks:
            if self.rect.colliderect(block):
                if self in self.tank.bullets_flight:
                    self.tank.bullets.append(self.tank.bullets_flight.pop(self.tank.bullets_flight.index(self)))
                if block.type_block == 1:
                    self.tank.game.blocks.remove(block)
                    game_map[block.y][block.x] = 0

    def update_cord(self):
        self.rect.x = self.tank.rect.x + self.tank.rect.width // 2 - self.rect.width // 2
        self.rect.y = self.tank.rect.y + self.tank.rect.height // 2 - self.rect.height // 2

        if self.tank.angle == 0:
            self.speed_x = 0
            self.speed_y = -self.speed
        elif self.tank.angle == 90:
            self.speed_x = -self.speed
            self.speed_y = 0
        elif self.tank.angle == 270:
            self.speed_x = self.speed
            self.speed_y = 0
        elif self.tank.angle == 180:
            self.speed_x = 0
            self.speed_y = self.speed


    def draw_count(self):
        self.tank.game.main_screen.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x += self.speed_x; self.rect.y += self.speed_y
        self.check_collide_count()
    

