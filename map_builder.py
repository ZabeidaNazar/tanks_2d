import pygame
import os
import json
from settings import *
from tank import *
from block import *
from camera import CameraGroup
from game_map import game_map
import pyautogui
import importlib
from pygame_menu.widgets import TextInput
import pygame_menu
from modes.mode_settings import MODE_DATA


pygame.init()
pygame.display.set_caption("Tanks | Map builder")


class MapBuilder:
    def __init__(self):
        self.main_screen = pygame.display.set_mode(RES, pygame.RESIZABLE)
        self.time = pygame.time.Clock()
        self.playing = True

        self.hand_active = False
        self.hand_pos = (0, 0)
        self.wheel_speed = 50

        self.maps_folder = get_path("modes/mode_1_player/levels")
        self.current_map = 0
        self.view()
        self.camera_group = CameraGroup(target="keyboard")

        self.new_text_game_map = [[0 for item in range(V_WIDTH // BLOCKSIZE)] for row in range(V_HEIGHT // BLOCKSIZE)]
        self.new_game_map = [[0 for item in range(V_WIDTH // BLOCKSIZE)] for row in range(V_HEIGHT // BLOCKSIZE)]

        self.level_data = {
            "tanks": {
                "simple tanks": [],
                "auto tanks": []
            },
            "blocks map": [[0 for _ in range(V_WIDTH // BLOCKSIZE)] for _ in range(V_HEIGHT // BLOCKSIZE)]
        }

        # self.keys = {
        #     pygame.K_t: "simple_tank",
        #     pygame.K_h: "hard_tank",
        #     pygame.K_1: "wall_s",
        #     pygame.K_2: "wall_h",
        # }

        self.now_action = None

        self.keys = {
            pygame.K_1: self.create_wall_1,
            pygame.K_2: self.create_wall_2,
            pygame.K_3: self.create_tank,
            pygame.K_4: self.create_auto_tank,
        }

        self.objects_surfs = {key: pygame.image.load(get_path(value["graphics"])) for key, value in MODE_DATA["objects"].items()}

    def print_game_map(self):
        for row in self.new_text_game_map:
            print(row)

    def create_tank(self, x, y):
        self.new_game_map[y][x] = Tank_Control(self, self.camera_group, None, "images/panzer.png", x, y, 5, True, 30)
        # self.new_text_game_map[y][x] = 5
        self.level_data["tanks"]["simple tanks"].append((x, y))

    def create_auto_tank(self, x, y):
        self.new_game_map[y][x] = TankAutoControl(self, self.camera_group, None, "images/enemy.png", x, y, 50, 1700, False, 10)
        # self.new_text_game_map[y][x] = 7
        self.level_data["tanks"]["auto tanks"].append((x, y))

    def create_wall_1(self, x, y):
        block = Block(self.camera_group, 1, "images/wall.png", x, y)
        block.main_screen = self.main_screen
        self.new_game_map[y][x] = block
        # self.new_text_game_map[y][x] = 1
        self.level_data["blocks map"][y][x] = 1

    def create_wall_2(self, x, y):
        block = Block(self.camera_group, 2, "images/wall1.png", x, y)
        block.main_screen = self.main_screen
        self.new_game_map[y][x] = block
        # self.new_text_game_map[y][x] = 2
        self.level_data["blocks map"][y][x] = 2

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    self.hand_active = True
                    self.hand_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2:
                    self.hand_active = False
            elif event.type == pygame.MOUSEWHEEL:
                if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                    self.camera_group.offset.x -= event.y * self.wheel_speed
                else:
                    self.camera_group.offset.y -= event.y * self.wheel_speed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.save()
                    self.view()
                elif event.key == pygame.K_TAB:
                    print(self.files)
                    if self.files:
                        name = self.files[self.current_map]
                        module = importlib.import_module("maps."+name[:-3])
                        print(module)
                        self.new_text_game_map = module.game_map
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_v:
                    self.print_game_map()

    def hand_move(self):
        if self.hand_active:
            pos = pygame.mouse.get_pos()
            self.camera_group.offset.x += self.hand_pos[0] - pos[0]
            self.camera_group.offset.y += self.hand_pos[1] - pos[1]
            self.hand_pos = pos

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
            x = int((x + self.camera_group.offset.x) // BLOCKSIZE)
            y = int((y + self.camera_group.offset.y) // BLOCKSIZE)
            if 0 > x or x > X_BLOCK_COUNT-1 or 0 > y or y > Y_BLOCK_COUNT-1:
                return
            if not self.new_game_map[y][x]:
                if self.now_action:
                    self.now_action(x, y)
        elif pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            x = int(x + self.camera_group.offset.x) // BLOCKSIZE
            y = int(y + self.camera_group.offset.y) // BLOCKSIZE
            if 0 > x or x > X_BLOCK_COUNT-1 or 0 > y or y > Y_BLOCK_COUNT-1:
                return
            if self.new_game_map[y][x]:
                self.camera_group.remove(self.new_game_map[y][x])
                self.new_game_map[y][x] = 0
                self.new_text_game_map[y][x] = 0

    def save(self):
#         "Введіть назву ігрової карти:"
#
#         input = TextInput('fg', default='', input_type=pygame_menu.locals.INPUT_TEXT)
#         input.set_position(20, 20)  # Встановлюємо розташування
#         input.update_font({
#             'size': 36,
#             'color': (255, 50, 50),
#             'background_color': (50, 100, 100),
#             'antialias': True,  # Включити згладжування шрифта (antialiasing)
#             'name': 'Arial',  # Ім'я шрифта
#             'selected_color': (0, 0, 255)  # Колір для вибраного поля
# })
#
#         print(input.get_width())
#         print(input.get_height())
#         while self.playing:
#             events = pygame.event.get()
#             for event in events:
#                 if event.type == pygame.QUIT:
#                     self.playing = False
#             pygame.draw.rect(self.main_screen, (255, 100, 100), (50, 50, 100, 100), 2)
#             input.update(events)
#             input.draw(self.main_screen)
#             if input.get_value():
#                 print(input.get_value())
#             pygame.display.flip()
#
#
#
#         return

        res = pyautogui.prompt(text="Введіть назву ігрової карти:")
        if res is None:
            return
        files = os.listdir(self.maps_folder)
        while res + ".json" in files:
            res = pyautogui.prompt(text="Така назва вже існує, повторіть спробу!\nВведіть назву ігрової карти:")
            if res is None:
                return
        if res:
            try:
                with open(f"{self.maps_folder}/{res}.json", "w") as file:
                    json.dump(self.level_data, file)
            except Exception as e:
                print(e)

    def run(self):
        self.camera_group.set_keyboard_speed(10)
        while self.playing:
            self.main_screen.fill((60, 60, 255))
            self.get_event()
            self.get_key()
            self.get_mouse()
            self.hand_move()

            self.camera_group.drawing()

            pygame.display.flip()
            pygame.display.set_caption(str(round(self.time.get_fps(), 0)))
            self.time.tick(60)     # 10


if __name__ == "__main__":
    game = MapBuilder()
    game.run()
