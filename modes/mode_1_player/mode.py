import json
import random
import time
import traceback

from menu import pause_loop, menus, Menu, Menus, ButtonIcon, ButtonText, Label, btn_settings_icon, Area, Picture
from settings import *
from block import *
from tank import *
from camera import *
import maps.first_big_map
from game_map import game_map


class Mode:
    def __init__(self, game):
        self.game = game
        self.menus = menus
        self.main_screen = pygame.display.get_surface()
        self.camera_group = CameraGroup()
        self.player_obstacles_group = pygame.sprite.Group()
        self.tanks_group = pygame.sprite.Group()
        self.bullets = []

        # levels
        self.last_level_number = 1
        self.create_levels_menu()

        def to_run(self):
            self.game.is_finished = True
            # self.game.finish_menu = self.game.lose_menu
            self.game.menus.run_loop(self.game.game.main_screen, self.game.game.time, "lose menu")

        self.tank = Tank_Control(self, (self.camera_group, self.tanks_group), self.player_obstacles_group,
                                 "images/panzer.png", *maps.first_big_map.simple_tank_1, 5, True, 30)
        self.tank.set_onclick(to_run, self.tank)
        self.bullets.append(self.tank.bullets_flight)
        self.blocks = None
        self.bot_count = 0
        self.setup()

        self.btn_pause = ButtonIcon(get_path("images\\pause_30_30.png"), WIDTH - 30 - 5, 5, 30, 30)
        self.btn_pause.set_onclick(menus.run_loop, self.main_screen, self.game.time, "pause")
        self.label_bot_counter = Label(10, 10, f"Bot: {self.bot_count}", rect_width=-1)

        self.finish_menu = None

        self.is_finished = False

        # general menu objects
        menu_background = Area(150, 30, 900, 700, 10, (96, 96, 96))
        btn_levels = ButtonText(738, 372, (30, 255, 30), border_radius=10, hover_color=hover_color,
                                text="Рівні", on_click=lambda: "levels menu",
                                font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
        btn_main_menu = ButtonText(750, 554, (30, 255, 30), border_radius=10, hover_color=hover_color,
                                   text="Меню", on_click=lambda: "menu",
                                   font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)

        # create win menu
        self.win_menu = Menu("win menu")
        label_win = Label(WIDTH / 2, 35, center_x=True, rect_width=-1,
                          text="Вам вдалося! Ви здолали\nатаку ботів",
                          font_family="fonts/PressStart2P-Regular.ttf", font_color=(2, 79, 0), font_size=32)
        picture_win = Picture(get_path("images/pass.png"), 260, 215, 350, 350)
        btn_next_level = ButtonText(750, 190, (30, 255, 30), border_radius=10, hover_color=hover_color,
                                    text="Далі", on_click=lambda: "menu exit",
                                    font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
        self.win_menu.add_item(menu_background, label_win, picture_win,
                               btn_next_level, btn_levels, btn_main_menu, btn_settings_icon)

        # create lose menu
        self.lose_menu = Menu("lose menu")
        label_lose = Label(WIDTH / 2, 35, center_x=True, rect_width=-1,
                           text="Нажаль, боти виявилися\nсильнішими!",
                           font_family="fonts/PressStart2P-Regular.ttf", font_color=(79, 0, 0), font_size=32)
        picture_lose = Picture(get_path("images/fail.png"), 260, 215, 350, 350)
        btn_restart = ButtonText(726, 190, (30, 255, 30), border_radius=10, hover_color=hover_color,
                                 text="Заново", on_click=self.restart,
                                 font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
        self.lose_menu.add_item(menu_background, label_lose, picture_lose,
                                btn_restart, btn_levels, btn_main_menu, btn_settings_icon)

        menus.add_submenu(self.win_menu, self.lose_menu)

    def setup(self):
        blocks = []
        x = 0
        y = 0
        bot = 0

        def to_run(self):
            self.game.bot_count -= 1
            self.remove(self.groups())
            self.game.tanks_group.remove(self)
            self.game.label_bot_counter.set_text(f"Bot: {self.game.bot_count}")
            if self.game.bot_count == 0:
                self.game.is_finished = True
                # self.game.finish_menu = self.game.win_menu
                self.game.menus.run_loop(self.game.game.main_screen, self.game.game.time, "win menu")

        for row in game_map:
            for item in row:
                if item == 1:
                    blocks.append(Block((self.camera_group, self.player_obstacles_group), 1, "images/wall.png", x, y))
                elif item == 2:
                    blocks.append(Block((self.camera_group, self.player_obstacles_group), 2, "images/wall1.png", x, y))
                elif item == 0 or item == 7:
                    # blocks.append(  Block(0, "", x, y)  )
                    pass
                elif item == 8:
                    tank = TankAutoControl(self, (self.camera_group, self.player_obstacles_group, self.tanks_group),
                                           self.tank, "images/enemy.png", x, y, 50, random.randint(800, 1700),
                                           False, 10)
                    tank.set_onclick(to_run, tank)
                    bot += 1
                    self.bullets.append(tank.bullets_flight)
                else:
                    print(f"Incorrect value: '{item}'")
                x += 1

            x = 0
            y += 1

        self.blocks = blocks
        print(len(blocks))
        self.bot_count = bot

    def create_levels_menu(self):
        levels_menu = Menu("levels menu", background_color)
        label_levels = Label(WIDTH / 2, 55, center_x=True, rect_width=-1,
                             text="Рівні",
                             font_family="fonts/PressStart2P-Regular.ttf", font_color=(0, 0, 0), font_size=48)

        levels_path = os.listdir("modes/mode_1_player/levels")

        # create level buttons
        level_button = []
        x = 100
        y = 160
        width = 70
        height = 70
        max_count_on_row = 7
        count_on_row = 0
        gap = 85

        for level in levels_path:
            level_button.append(ButtonText(x, y, (30, 255, 30), hover_color=hover_color,
                                           border_radius=10, shift_x=20.5, shift_y=3.5,
                                           text=str(self.last_level_number), on_click=self.load_level, args=(level,),
                                           font_family="fonts/FiraCode-Regular.ttf", font_color=(0, 0, 0), font_size=48))
            count_on_row += 1
            if count_on_row == max_count_on_row:
                y += height + gap
                x -= (count_on_row-1) * (width + gap)
            else:
                x += width + gap

            self.last_level_number += 1

        # add item to menu
        levels_menu.add_item(label_levels, *level_button, btn_settings_icon)

        # add menu to main menu
        menus.add_submenu(levels_menu)

    def load_level(self, level_name):
        assert level_name in os.listdir(get_path("modes/mode_1_player/levels"))
        try:
            with open(get_path(f"modes/mode_1_player/levels/{level_name}"), "r") as file:
                data = json.load(file)
            self.setup_level_from_data(data)
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
        return "menu exit"

    def setup_level_from_data(self, data):
        self.camera_group.empty()
        self.player_obstacles_group.empty()
        self.tanks_group.empty()
        self.bullets.clear()
        self.blocks.clear()

        def to_run(self):
            self.game.is_finished = True
            # self.game.finish_menu = self.game.lose_menu
            self.game.menus.run_loop(self.game.game.main_screen, self.game.game.time, "lose menu")

        if data["tanks"]["simple tanks"]:
            self.tank = Tank_Control(self, (self.camera_group, self.tanks_group), self.player_obstacles_group,
                                     "images/panzer.png", *data["tanks"]["simple tanks"], 5, True, 30)
        else:
            self.tank = Tank_Control(self, (self.camera_group, self.tanks_group), self.player_obstacles_group,
                                     "images/panzer.png", X_BLOCK_COUNT//2, Y_BLOCK_COUNT//2, 5, True, 30)
            data["blocks map"][Y_BLOCK_COUNT//2][X_BLOCK_COUNT//2] = 0
        self.tank.set_onclick(to_run, self.tank)
        self.bullets.append(self.tank.bullets_flight)

        self.bot_count = 0

        def to_run(self):
            self.game.bot_count -= 1
            self.remove(self.groups())
            self.game.tanks_group.remove(self)
            self.game.label_bot_counter.set_text(f"Bot: {self.game.bot_count}")
            if self.game.bot_count == 0:
                self.game.is_finished = True
                # self.game.finish_menu = self.game.win_menu
                self.game.menus.run_loop(self.game.game.main_screen, self.game.game.time, "win menu")

        for t_x, t_y in data["tanks"]["auto tanks"]:
            tank = TankAutoControl(self, (self.camera_group, self.player_obstacles_group, self.tanks_group),
                                   self.tank, "images/enemy.png", t_x, t_y, 50, random.randint(800, 1700),
                                   False, 10)
            tank.set_onclick(to_run, tank)
            self.bullets.append(tank.bullets_flight)
            self.bot_count += 1

        self.label_bot_counter.set_text(f"Bot: {self.bot_count}")

        x = 0
        y = 0

        for row in data["blocks map"]:
            for item in row:
                if item == 1:
                    self.blocks.append(Block((self.camera_group, self.player_obstacles_group), 1, "images/wall.png", x, y))
                elif item == 2:
                    self.blocks.append(Block((self.camera_group, self.player_obstacles_group), 2, "images/wall1.png", x, y))
                elif item == 0:
                    pass
                else:
                    print(f"Incorrect value: '{item}'")
                x += 1

            x = 0
            y += 1

        self.is_finished = False

    def restart(self):
        print("restart")

    def run(self):
        self.main_screen.fill((30, 30, 255))
        self.camera_group.drawing(self.tank)

        self.label_bot_counter.draw(self.main_screen)
        self.btn_pause.check_click()
        self.btn_pause.draw(self.main_screen)

        if not self.is_finished:
            self.camera_group.update()
            for tank in self.tanks_group:
                tank.check_collide(self.bullets)
        # else:
        #     self.finish_menu.draw(self.main_screen)