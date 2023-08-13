import pygame
import os
import random
import json
from settings import *
from tank import *
from block import *
from camera import CameraGroup
from base import ButtonWithImage, ButtonIcon, Area, Label, ButtonText
from menu import Menu, menus
from windows import *

pygame.init()
pygame.display.set_caption(editor_caption)


class MapBuilder:
    def __init__(self):
        self.main_screen = pygame.display.set_mode(RES, pygame.RESIZABLE)
        self.time = pygame.time.Clock()
        self.playing = True

        self.hand_active = False
        self.hand_pos = (0, 0)
        self.wheel_speed = 50

        # menus
        self.create_menus()

        self.maps_folder = get_path("modes/mode_1_player/levels")
        self.current_map = 0
        self.view()

        # create game elements
        self.camera_group = CameraGroup(target="keyboard")
        self.camera_group.set_keyboard_speed(10)
        self.player_obstacles_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        self.new_game_map = [[0 for _ in range(V_WIDTH // BLOCKSIZE)] for _ in range(V_HEIGHT // BLOCKSIZE)]

        # create cache dict
        self.cache = {
            "simple tanks": [],
            "auto tanks": [],
            "1 blocks": [],
            "2 blocks": []
        }

        # self.keys = {
        #     pygame.K_1: "1 block",
        #     pygame.K_2: "2 block",
        #     pygame.K_3: "simple tank",
        #     pygame.K_4: "auto tank",
        # }

        self.now_action = None

        self.keys = {
            pygame.K_1: self.create_wall_1,
            pygame.K_2: self.create_wall_2,
            pygame.K_3: self.create_tank,
            pygame.K_4: self.create_auto_tank,
        }

    def set_now_action(self, action):
        self.now_action = action

    def create_tank(self, x, y):
        if self.cache["simple tanks"]:
            tank = self.cache["simple tanks"].pop()
            tank.rect.x = tank.start_x = x * BLOCKSIZE
            tank.rect.y = tank.start_y = y * BLOCKSIZE
            tank.add(*tank.sprite_groups)
        else:
            Tank_Control(self, (self.camera_group, self.player_group), self.new_game_map,
                         self.player_obstacles_group,
                         "images/panzer.png", x, y, 5, True, 30)

    def create_auto_tank(self, x, y):
        if self.cache["auto tanks"]:
            tank = self.cache["auto tanks"].pop()
            tank.rect.x = tank.start_x = x * BLOCKSIZE
            tank.rect.y = tank.start_y = y * BLOCKSIZE
            tank.add(*tank.sprite_groups)
        else:
            TankAutoControl(self, (self.camera_group, self.player_obstacles_group, self.enemies_group),
                            None, self.new_game_map,
                            "images/enemy.png", x, y, 50, random.randint(500, 900), False, 10)

    def create_wall_1(self, x, y):
        if self.cache["1 blocks"]:
            block = self.cache["1 blocks"].pop()
            block.rect.x = x * BLOCKSIZE
            block.rect.y = y * BLOCKSIZE
            block.add(*block.sprite_groups)
        else:
            Block((self.camera_group, self.player_obstacles_group, self.blocks), self.new_game_map,
                  1, "images/wall.png", x, y)
        self.new_game_map[y][x] = 1
        # self.level_data["blocks map"][y][x] = 1

    def create_wall_2(self, x, y):
        if self.cache["2 blocks"]:
            block = self.cache["2 blocks"].pop()
            block.rect.x = x * BLOCKSIZE
            block.rect.y = y * BLOCKSIZE
            block.add(*block.sprite_groups)
        else:
            Block((self.camera_group, self.player_obstacles_group, self.blocks), self.new_game_map,
                  2, "images/wall1.png", x, y)
        self.new_game_map[y][x] = 2
        # self.level_data["blocks map"][y][x] = 2

    def home(self):
        self.main_screen = pygame.display.set_mode(RES)
        self.playing = False
        menus.run_loop(self.main_screen, self.time)

    def create_menus(self):
        # settings menu
        self.settings_menu = Menu("editor settings menu", background_color)
        sett_editor_info = Label(0, 0, editor_info, bg_color=(100, 180, 180), shift_x=20, shift_y=20, line_space=0,
                                 width=1000)
        btn_back = ButtonText(WIDTH // 2, 530, (30, 255, 30), "Назад", font_color=(20, 20, 255), font_size=40,
                              border_radius=10,
                              hover_color=hover_color, center_x=True)
        btn_back.set_onclick(lambda: "menu exit")
        self.settings_menu.add_item(sett_editor_info, btn_back)

        # elements menu
        self.elements_menu = Menu("elements menu", (100, 100, 100))

        menu_background = Area(0, 0, 400, 80, -1, (96, 96, 96))

        btn_home_icon = ButtonIcon("images/home_icon_25_25.png", 10, 7, 25, 25,
                                   on_click=self.home)
        btn_open_icon = ButtonIcon("images/folder_25_16.png", 10, 56, 25, 16,
                                   on_click=self.open)
        btn_info_icon = ButtonIcon("images/info_icon_25_25.png", 50, 7, 25, 25,
                                   on_click=self.settings_menu.run_loop, args=(self.main_screen, self.time))
        btn_save_icon = ButtonIcon("images/save_icon_25_25.png", 50, 47, 25, 25,
                                   on_click=self.save)

        btn_block_1 = ButtonWithImage(100, 7, 65, 65, "images/wall.png", 50, 50, BUTTON_BG_COLOR,
                                      active_color=BUTTON_LINE_COLOR,
                                      on_click=self.set_now_action, args=(self.create_wall_1, ))
        btn_block_2 = ButtonWithImage(175, 7, 65, 65, "images/wall1.png", 50, 50, BUTTON_BG_COLOR,
                                      active_color=BUTTON_LINE_COLOR,
                                      on_click=self.set_now_action, args=(self.create_wall_2, ))
        btn_simple_tank = ButtonWithImage(250, 7, 65, 65, "images/panzer.png", 50, 50, BUTTON_BG_COLOR,
                                          active_color=BUTTON_LINE_COLOR,
                                          on_click=self.set_now_action, args=(self.create_tank, ))
        btn_auto_tank = ButtonWithImage(325, 7, 65, 65, "images/enemy.png", 50, 50, BUTTON_BG_COLOR,
                                        active_color=BUTTON_LINE_COLOR,
                                        on_click=self.set_now_action, args=(self.create_auto_tank, ))

        self.buttons = [btn_block_1, btn_block_2, btn_simple_tank, btn_auto_tank]

        self.elements_menu.add_item(menu_background,
                                    btn_home_icon, btn_open_icon, btn_info_icon, btn_save_icon,
                                    btn_block_1, btn_block_2, btn_simple_tank, btn_auto_tank)

        setattr(self.elements_menu, "rect", menu_background.rect)

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.save()
                    self.view()
                elif event.key == pygame.K_r:
                    print()
                elif event.key == pygame.K_TAB:
                    print(self.files)
                    # if self.files:
                    #     name = self.files[self.current_map]
            self.elements_menu.update(event)

    def get_key(self):
        keys = pygame.key.get_pressed()
        for key in self.keys:
            if keys[key]:
                self.now_action = self.keys[key]
                current_btn = self.buttons[list(self.keys).index(key)]
                for button in self.buttons:
                    if button is current_btn:
                        continue
                    button.dis_activated()
                current_btn.activated()

    def get_mouse(self):
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            if self.elements_menu.rect.collidepoint(x, y):
                return
            x = int(x + self.camera_group.offset.x)
            y = int(y + self.camera_group.offset.y)
            if 0 > x or x > V_WIDTH or 0 > y or y > V_HEIGHT:
                return
            for sprite in self.camera_group:
                if sprite.rect.collidepoint(x, y):
                    return
            if self.now_action:
                self.now_action(x // BLOCKSIZE, y // BLOCKSIZE)
        elif pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            x = x + int(self.camera_group.offset.x)
            y = y + int(self.camera_group.offset.y)
            if 0 > x or x > V_WIDTH or 0 > y or y > V_HEIGHT:
                return

            for block in self.blocks:
                if block.rect.collidepoint(x, y):
                    block.kill()
                    if block.type_block == 1:
                        self.cache["1 blocks"].append(block)
                    elif block.type_block == 2:
                        self.cache["2 blocks"].append(block)
                    self.new_game_map[y // BLOCKSIZE][x // BLOCKSIZE] = 0
                    return

            for tank in self.enemies_group:
                if tank.rect.collidepoint(x, y):
                    tank.kill()
                    self.cache["auto tanks"].append(tank)
                    return

            for tank in self.player_group:
                if tank.rect.collidepoint(x, y):
                    tank.kill()
                    self.cache["simple tanks"].append(tank)
                    return

    def hand_move(self):
        if self.hand_active:
            pos = pygame.mouse.get_pos()
            self.camera_group.offset.x += self.hand_pos[0] - pos[0]
            self.camera_group.offset.y += self.hand_pos[1] - pos[1]
            self.hand_pos = pos

    def view(self):
        self.files = os.listdir(self.maps_folder)
        for file in self.files.copy():
            if not file.endswith(".json"):
                self.files.remove(file)
            elif os.path.isdir(f"{self.maps_folder}\{file}"):
                self.files.remove(file)

    def save(self):
        res, ok = get_text_input("Введіть назву рівня:")
        if not ok:
            return
        elif res == "":
            show_mess("Ви не ввели назву рівня!")
            return

        files = os.listdir(self.maps_folder)
        while res + ".json" in files:
            res, ok = get_text_input("Така назва вже існує, повторіть спробу!\nВведіть назву ігрової карти:")
            if not ok:
                return

        level_data = {
            "tanks": {
                "simple tanks": [(tank.start_x // BLOCKSIZE, tank.start_y // BLOCKSIZE) for tank in
                                 self.player_group],
                "auto tanks": [(tank.start_x // BLOCKSIZE, tank.start_y // BLOCKSIZE) for tank in
                               self.enemies_group]
            },
            "blocks map": self.new_game_map
        }

        try:
            with open(f"{self.maps_folder}/{res}.json", "w") as file:
                json.dump(level_data, file, indent=4)
        except Exception as e:
            print(e)

    def open(self):
        self.view()
        print(get_select_input(self.files))

    def run(self):
        while self.playing:
            self.main_screen.fill((60, 60, 255))
            self.get_event()
            self.get_key()
            self.get_mouse()
            self.hand_move()

            self.camera_group.drawing(self.camera_group)

            self.elements_menu.draw(window=self.main_screen)

            pygame.display.flip()
            pygame.display.set_caption(f"{editor_caption}  fps:  {str(round(self.time.get_fps(), 0))}")
            self.time.tick(60)
