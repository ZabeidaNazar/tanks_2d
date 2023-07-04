import pygame
from settings import *
from tank import *
from block import *
from camera import CameraGroup


pygame.init()
pygame.display.set_caption("Tanks")


import maps.maza_first
auto_tank_1 = maps.maza_first.auto_tank_1
simple_tank_1 = maps.maza_first.simple_tank_1


class Game:
    def __init__(self):
        self.main_screen = pygame.display.set_mode(RES)
        self.time = pygame.time.Clock()
        self.playing = True
        self.background_image = pygame.transform.scale(pygame.image.load("images/background.png").convert_alpha(), RES)
        self.camera_group = CameraGroup()


        self.tank = Tank_Control(self, None, "images/panzer.png", *simple_tank_1, BLOCKSIZE, False, 30)
        self.tank_enemy = TankAutoControl(self, None, "images/enemy.png", *auto_tank_1, BLOCKSIZE, False, 10)
        self.tanks = (self.tank, self.tank_enemy)
        self.blocks = get_blocks(None)
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
            elif not self.tank.can_do_bullet:
                if event.type == self.tank.CREAT_BULLET:
                    self.tank.can_do_bullet = True
            if not self.is_kill:
                if event.type == self.BOT_MOVE:
                    self.tank_enemy.move(enemy=self.tank)
                if event.type == self.PLAYER_MOVE:
                    self.tank.go()
                    # pass                    
                

    def run(self):
        while self.playing:
            self.get_event()
            # self.main_screen.fill((30, 30, 255))
            self.main_screen.blit(self.background_image, (0, 0))

                       
            for block in self.blocks:
                self.main_screen.blit(block.image, (block.rect.x, block.rect.y))

            self.tank_enemy.draw_count()
            self.tank.draw_count()


            if not self.is_kill:
                # self.tank.go()
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