import pygame
from settings import *
from tank import *
from block import *
from camera import CameraGroup
import time


pygame.init()
pygame.display.set_caption("Tanks")


import maps.first_big_map
auto_tank_1 = maps.first_big_map.auto_tank_1
simple_tank_1 = maps.first_big_map.simple_tank_1


class Game:
    def __init__(self):
        self.main_screen = pygame.display.set_mode(RES)
        self.time = pygame.time.Clock()
        self.playing = True
        # self.background_image = pygame.transform.scale(pygame.image.load("images/background.png").convert_alpha(), RES)
        self.camera_group = CameraGroup()
        self.obstracles_group = pygame.sprite.Group()


        self.tank = Tank_Control(self, self.camera_group, self.obstracles_group, "images/panzer.png", *simple_tank_1, 5, True, 30)
        self.tank_enemy = TankAutoControl(self, (self.camera_group, self.obstracles_group), "images/enemy.png", *auto_tank_1, 50, False, 10)
        self.tanks = (self.tank, self.tank_enemy)
        self.blocks = get_blocks((self.camera_group, self.obstracles_group))
        print(len(self.blocks))

        self.BOT_MOVE = pygame.USEREVENT + 2
        pygame.time.set_timer(self.BOT_MOVE, BOT_SPEED)

        self.PLAYER_MOVE = pygame.USEREVENT + 3
        pygame.time.set_timer(self.PLAYER_MOVE, PLAYER_SPEED)


        self.is_kill = False



    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if not self.is_kill:
                if event.type == self.BOT_MOVE:
                    self.tank_enemy.move(enemy=self.tank)
                # if event.type == self.PLAYER_MOVE:
                #     self.tank.go()
                    # pass                    
                

    def run(self):
        while self.playing:
            self.get_event()
            self.main_screen.fill((30, 30, 255))
            # self.main_screen.blit(self.background_image, (0, 0))

            # self.tank_enemy.draw_count()
            # self.tank.draw_count()

            self.camera_group.drawing(self.tank)
            self.camera_group.update()


            if not self.is_kill:
                self.tank_enemy.check_collide(self.tank.bullets_flight)
                self.tank.check_collide(self.tank_enemy.bullets_flight)


            # self.tank_enemy.draw_point()
            # self.tank_enemy.draw_path()

               
            pygame.display.flip()
            pygame.display.set_caption(str(self.time.get_fps()))

            self.time.tick(30)     # 10


if __name__ == "__main__":
    game = Game()
    game.run()