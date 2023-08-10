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
        # base setup
        self.game = game
        self.menus = menus
        self.main_screen = pygame.display.get_surface()

        # create game elements
        self.camera_group = CameraGroup()
        self.player_obstacles_group = pygame.sprite.Group()
        self.tanks_group = pygame.sprite.Group()
        self.enemies_group = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        self.levels_cache = {}
        self.last_level = None
        self.bot_count = 0

        # create pause icon
        self.btn_pause = ButtonIcon(get_path("images\\pause_30_30.png"), WIDTH - 30 - 5, 5, 30, 30)
        self.btn_pause.set_onclick(menus.run_loop, self.main_screen, self.game.time, "pause")

        # create label for count of bot
        self.label_bot_counter = Label(10, 10, f"Bot: {self.bot_count}", rect_width=-1)

        # levels menu
        self.create_levels_menu()

        # create pause menu
        self.create_pause_menu()

        # finish level flag
        self.is_finished = False

        # finish level menus
        # create general menu objects
        menu_background = Area(150, 30, 900, 700, 10, (96, 96, 96))
        btn_levels = ButtonText(738, 372, (30, 255, 30), border_radius=10, hover_color=hover_color,
                                text="Рівні", on_click=lambda: "levels menu",
                                font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
        btn_main_menu = ButtonText(750, 554, (30, 255, 30), border_radius=10, hover_color=hover_color,
                                   text="Меню", on_click=lambda: "menu",
                                   font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)

        # create win menu
        self.win_menu = Menu("win menu", None)
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
        self.lose_menu = Menu("lose menu", None)
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

        # load first level
        self.load_level("1.json")

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

        for level_number, level in enumerate(levels_path, 1):
            level_button.append(ButtonText(x, y, (30, 255, 30), hover_color=hover_color,
                                           border_radius=10, shift_x=20.5, shift_y=3.5,
                                           text=str(level_number), on_click=self.load_level, args=(level,),
                                           font_family="fonts/FiraCode-Regular.ttf", font_color=(0, 0, 0), font_size=48))
            count_on_row += 1
            if count_on_row == max_count_on_row:
                y += height + gap
                x -= (count_on_row-1) * (width + gap)
            else:
                x += width + gap

        # add item to menu
        levels_menu.add_item(label_levels, *level_button, btn_settings_icon)

        # add menu to main menu
        menus.add_submenu(levels_menu)

    def create_pause_menu(self):
        # create menu with transparent background
        pause_menu = Menu("pause", None)

        # Створення елементів, які будуть відображатися в меню паузи
        btn_play = ButtonIcon("images\\play_30_30.png", WIDTH - 30 - 5, 5, 30, 30, on_click=None)
        btn_play.set_onclick(lambda: "menu exit")
        btn_continue = ButtonText(WIDTH // 2, 100, (30, 255, 30), "Продовжити", font_color=(20, 20, 255), font_size=40,
                                  border_radius=10, hover_color=hover_color, center=True)
        btn_continue.set_onclick(lambda: "menu exit")
        btn_restart = ButtonText(WIDTH // 2, 260, (30, 255, 30), "Почати заново", font_color=(20, 20, 255),
                                 font_size=40,
                                 border_radius=10, hover_color=hover_color, center=True)
        btn_restart.set_onclick(self.restart)
        btn_menu = ButtonText(WIDTH // 2, 420, (30, 255, 30), "Головне меню", font_color=(20, 20, 255), font_size=40,
                              border_radius=10, hover_color=hover_color, center=True)
        btn_menu.set_onclick(lambda: "menu")

        # add item to menu
        pause_menu.add_item(btn_play, btn_continue, btn_restart, btn_menu)

        # add menu to main menu
        menus.add_submenu(pause_menu)

    def load_level(self, level_name):
        assert level_name in os.listdir(get_path("modes/mode_1_player/levels"))
        if level_name not in self.levels_cache:
            try:
                with open(get_path(f"modes/mode_1_player/levels/{level_name}"), "r") as file:
                    data = json.load(file)
                self.setup_level_from_data(data, level_name)
            except Exception as e:
                print("Error:")
                traceback.print_exception(type(e), e, e.__traceback__)
        else:
            self.setup_level_from_cache(level_name)
        return "menu exit"

    def setup_level_from_data(self, data, level_name):
        self.camera_group.empty()
        self.player_obstacles_group.empty()
        self.tanks_group.empty()
        self.enemies_group.empty()
        self.blocks.empty()

        cache = []

        if data["tanks"]["simple tanks"]:
            self.tank = Tank_Control(self, (self.camera_group, self.tanks_group), data["blocks map"], self.player_obstacles_group,
                                     "images/panzer.png", *data["tanks"]["simple tanks"][0], 5, True, 30)
        else:
            self.tank = Tank_Control(self, (self.camera_group, self.tanks_group), data["blocks map"], self.player_obstacles_group,
                                     "images/panzer.png", X_BLOCK_COUNT//2, Y_BLOCK_COUNT//2, 5, True, 30)
            data["blocks map"][Y_BLOCK_COUNT//2][X_BLOCK_COUNT//2] = 0
        cache.append(self.tank)

        self.bot_count = 0

        for t_x, t_y in data["tanks"]["auto tanks"]:
            tank = TankAutoControl(self, (self.camera_group, self.player_obstacles_group, self.tanks_group, self.enemies_group),
                                   self.tank, data["blocks map"], "images/enemy.png", t_x, t_y, 50, random.randint(500, 900),
                                   False, 10)
            self.bot_count += 1
            cache.append(tank)

        self.label_bot_counter.set_text(f"Bot: {self.bot_count}")

        x = 0
        y = 0

        for row in data["blocks map"]:
            for item in row:
                if item == 1:
                    block = Block((self.camera_group, self.player_obstacles_group, self.blocks), data["blocks map"], 1, "images/wall.png", x, y)
                    cache.append(block)
                elif item == 2:
                    block = Block((self.camera_group, self.player_obstacles_group, self.blocks), data["blocks map"], 2, "images/wall1.png", x, y)
                    cache.append(block)
                elif item == 0:
                    pass
                else:
                    print(f"Incorrect value: '{item}'")
                x += 1

            x = 0
            y += 1

        self.levels_cache[level_name] = cache
        self.last_level = level_name

        self.is_finished = False

    def setup_level_from_cache(self, level_name):
        cache = self.levels_cache[level_name]

        self.camera_group.empty()
        self.player_obstacles_group.empty()
        self.tanks_group.empty()
        self.enemies_group.empty()
        self.blocks.empty()

        print("reset")

        for element in cache:
            element.reset()

        self.last_level = level_name

        self.is_finished = False

    def get_damage(self):
        for tank in self.enemies_group:
            if tank.check_bullet_collide(self.tanks_group):
                tank.kill()
                self.bot_count -= 1
                self.label_bot_counter.set_text(f"Bot: {self.bot_count}")
                if self.bot_count == 0:
                    self.is_finished = True
                    self.menus.run_loop(self.main_screen, self.game.time, "win menu")

        if self.tank.check_bullet_collide(self.tanks_group):
            self.is_finished = True
            self.menus.run_loop(self.main_screen, self.game.time, "lose menu")

    def restart(self):
        self.setup_level_from_cache(self.last_level)
        return "menu exit"

    def run(self):
        self.main_screen.fill((30, 30, 255))
        self.camera_group.drawing(self.tank)

        self.label_bot_counter.draw(self.main_screen)
        self.btn_pause.check_click()
        self.btn_pause.draw(self.main_screen)

        if not self.is_finished:
            self.camera_group.update()
            self.get_damage()
        # else:
        #     self.finish_menu.draw(self.main_screen)
