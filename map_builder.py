import pygame
import os
import datetime
from time import time
from settings import *
from tank import *
from block import *
from game_map import game_map
import pyautogui
import importlib


pygame.init()
pygame.display.set_caption("Tanks | Map builder")


class MapBuilder:
    def __init__(self):
        self.main_screen = pygame.display.set_mode(RES)
        self.time = pygame.time.Clock()
        self.playing = True
        self.background_image = pygame.transform.scale(pygame.image.load("images/background.png"), RES)
        self.maps_folder = f"{PATH}\maps"
        self.current_map = 0
        self.view()
        # self.data = datetime.datetime()

        Block.draw = lambda self: self.main_screen.blit(self.image, (self.rect.x, self.rect.y))


        self.tank = Tank_Control(self, "images/panzer.png", 20, 13, BLOCKSIZE, True)
        self.tank_enemy = TankAutoControl(self, "images/enemy.png", 1, 1, BLOCKSIZE, False)

        self.blocks = []
        self.elements = []

        self.new_text_game_map = [ [ 0 for item in range(len(game_map[row]))] for row in range(len(game_map)) ]
        self.new_game_map = [ [ 0 for item in range(len(game_map[row]))] for row in range(len(game_map)) ]

        # self.keys = {
        #     pygame.K_t: "simple_tank",
        #     pygame.K_h: "hard_tank",
        #     pygame.K_1: "wall_s",
        #     pygame.K_2: "wall_h",
        # }

        self.now_action = None

        self.keys = {
            pygame.K_g: self.create_tank,
            pygame.K_h: self.create_auto_tank,
            pygame.K_q: self.create_wall_1,
            pygame.K_w: self.create_wall_2,
        }


    def create_tank(self, x, y):
        self.new_game_map[y][x] = Tank_Control(self, "images/panzer.png", x, y, BLOCKSIZE, True)
        self.new_text_game_map[y][x] = 5
        # self.elements.append(Tank_Control(self, "images/panzer.png", x, y, BLOCKSIZE, True))
    def create_auto_tank(self, x, y):
        self.new_game_map[y][x] = TankAutoControl(self, "images/enemy.png", x, y, BLOCKSIZE, False)
        self.new_text_game_map[y][x] = 7
        # self.elements.append(TankAutoControl(self, "images/enemy.png", x, y, BLOCKSIZE, False))
    def create_wall_1(self, x, y):
        block = Block(1, "images/wall.png", x, y)
        block.main_screen = self.main_screen
        self.new_game_map[y][x] = block
        self.new_text_game_map[y][x] = 1
        # self.blocks.append(block)
    def create_wall_2(self, x, y):
        block = Block(2, "images/wall1.png", x, y)
        block.main_screen = self.main_screen
        self.new_game_map[y][x] = block
        self.new_text_game_map[y][x] = 2
        # self.blocks.append(block)



    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.save()
                    self.view()
                elif event.key == pygame.K_LEFT:
                    if self.files:
                        name = self.files[self.current_map]
                        module = importlib.import_module("maps."+name[:-3])
                        self.new_text_game_map = module.game_map
                elif event.key == pygame.K_RIGHT:
                    pass
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     x, y = event.pos
            #     x //= BLOCKSIZE
            #     y //= BLOCKSIZE
            #     if event.button == 1:
            #         if self.now_action:
            #             self.now_action(x, y)
            #             print("blocks:", len(self.blocks))
            #             print("elements:", len(self.elements))
            #     elif event.button == 3:
            #         self.blocks()

    def view(self):
        self.files = os.listdir(self.maps_folder)
        for file in self.files:
            if not file.endswith(".py"):
                self.files.remove(file)
            elif os.path.isdir(f"{self.maps_folder}\{file}"):
                self.files.remove(file)

    

    def get_key(self):
        keys = pygame.key.get_pressed()
        for key in self.keys:
            if keys[key]:
                self.now_action = self.keys[key]

    def get_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            x //= BLOCKSIZE
            y //= BLOCKSIZE
            if not self.new_game_map[y][x]:
                if self.now_action:
                    self.now_action(x, y)
        elif pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            x //= BLOCKSIZE
            y //= BLOCKSIZE
            if self.new_game_map[y][x]:
                self.new_game_map[y][x] = 0
                self.new_text_game_map[y][x] = 0

    
    def save(self):
        res = pyautogui.prompt(text="Введіть назву ігрової карти:")
        if res is None:
            return
        files = os.listdir(self.maps_folder)
        while res + ".py" in files:
            res = pyautogui.prompt(text="Така назва вже існує, повторіть спробу!\nВведіть назву ігрової карти:")
            if res is None:
                return
        if res:
            try:
                # str(time())
                map_text = "game_map = [\n"
                for row in self.new_text_game_map:
                    map_text += "\t" + str(row).replace("5", "0").replace("7", "0") + ",\n"

                map_text += "]\n\n\n"
                
                simple_tanks_count = 1
                x = 0
                y = 0
                for row in self.new_text_game_map:
                    for item in row:
                        if item == 7:
                            map_text += f"simple_tank_{simple_tanks_count} = ({x}, {y})\n"
                            simple_tanks_count += 1
                        x += 1
                    y += 1
                    x = 0

                auto_tanks_count = 1                
                x = 0
                y = 0
                for row in self.new_text_game_map:
                    for item in row:
                        if item == 5:
                            map_text += f"auto_tank_{auto_tanks_count} = ({x}, {y})\n"
                            auto_tanks_count += 1
                        x += 1
                    y += 1
                    x = 0

                with open(f"{self.maps_folder}/{res}.py", "w") as file:
                    file.write(map_text)
            except Exception as e:
                print(e)


            

    def run(self):
        while self.playing:
            self.get_event()
            self.get_key()
            self.get_mouse()
            self.main_screen.blit(self.background_image, (0, 0))

                       
            # for block in self.blocks:
            #     self.main_screen.blit(block.image, (block.rect.x, block.rect.y))

            # for item in self.elements:
            #     item.draw()
            for row in self.new_game_map:
                for item in row:
                    if item != 0:
                        item.draw()

               
            pygame.display.flip()
            pygame.display.set_caption(str(round(self.time.get_fps(), 0)))

            self.time.tick(30)     # 10


if __name__ == "__main__":
    game = MapBuilder()
    game.run()