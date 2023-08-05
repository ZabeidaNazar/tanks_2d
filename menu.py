import pygame
from settings import *
from base import ButtonText, ButtonIcon, Label, Area, Picture

# створення кнопок меню
btn_start = ButtonText(WIDTH // 2, 100, (30, 255, 30), "Старт", font_color=(20, 20, 255), font_size=40,
                       border_radius=10,
                       hover_color=hover_color, center=True)
btn_settings = ButtonText(WIDTH // 2, 260, (30, 255, 30), "Налаштування", font_color=(20, 20, 255), font_size=40,
                          border_radius=10, hover_color=hover_color, center=True)
btn_exit = ButtonText(WIDTH // 2, 420, (30, 255, 30), "Вихід", font_color=(20, 20, 255), font_size=40, border_radius=10,
                      hover_color=hover_color, center=True)
btn_back = ButtonText(WIDTH // 2, 530, (30, 255, 30), "Назад", font_color=(20, 20, 255), font_size=40, border_radius=10,
                      hover_color=hover_color, center=True)

# Створення елементів налаштувань
sett_game_info = Label(0, 0, about_game, bg_color=(100, 180, 180), shift_x=20, shift_y=20, line_space=0, width=1000)

# Створення елементів, які будуть відображатися в меню паузи
btn_play = ButtonIcon("images\\play_30_30.png", WIDTH - 30 - 5, 5, 30, 30, on_click=None)
btn_continue = ButtonText(WIDTH // 2, 100, (30, 255, 30), "Продовжити", font_color=(20, 20, 255), font_size=40,
                          border_radius=10, hover_color=hover_color, center=True)

btn_restart = ButtonText(WIDTH // 2, 260, (30, 255, 30), "Почати заново", font_color=(20, 20, 255), font_size=40,
                         border_radius=10, hover_color=hover_color, center=True)
btn_menu = ButtonText(WIDTH // 2, 420, (30, 255, 30), "Головне меню", font_color=(20, 20, 255), font_size=40,
                      border_radius=10, hover_color=hover_color, center=True)


def main_menu(window, clock, screen, back=background_color):
    run = True
    pygame.display.set_caption(f"{window_title} - Меню")
    while run:

        window.fill(back)

        if screen == "menu":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if btn_start.check_collide(event.pos):
                        pygame.display.set_caption(window_title)
                        return "restart"
                    elif btn_settings.check_collide(event.pos):
                        screen = "settings"
                        pygame.display.set_caption(f"{window_title} - Налаштування")
                    elif btn_exit.check_collide(event.pos):
                        exit()
                elif event.type == pygame.MOUSEMOTION:
                    btn_start.hover(event.pos)
                    btn_settings.hover(event.pos)
                    btn_exit.hover(event.pos)

            btn_start.draw(window)
            btn_settings.draw(window)
            btn_exit.draw(window)

        elif screen == "settings":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if btn_back.check_collide(event.pos):
                        screen = "menu"
                        pygame.display.set_caption(f"{window_title} - Меню")
                elif event.type == pygame.MOUSEMOTION:
                    btn_back.hover(event.pos)

            btn_back.draw(window)
            sett_game_info.draw(window)

        pygame.display.update()
        clock.tick(menu_fps)


def pause_loop(window, clock):
    pygame.display.set_caption(f"{window_title} - Пауза")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # if btn_play.check_collide(event.pos) or btn_continue.check_collide(event.pos):
                #     pygame.display.set_caption(window_title)
                #     return
                if btn_restart.check_collide(event.pos):
                    pygame.display.set_caption(window_title)
                    return "restart"
                elif btn_menu.check_collide(event.pos):
                    pygame.display.set_caption(window_title)
                    return main_menu(window, clock, "menu")
            elif event.type == pygame.MOUSEMOTION:
                btn_continue.hover(event.pos)
                btn_restart.hover(event.pos)
                btn_menu.hover(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.display.set_caption(window_title)
                return

        # window.fill(back)

        btn_play.draw(window)
        btn_play.draw(window)
        btn_continue.draw(window)
        btn_restart.draw(window)
        btn_menu.draw(window)

        pygame.display.update()
        clock.tick(menu_fps)


class Menu:
    def __init__(self, screen="menu", background_color=(0, 0, 0), *items):
        self.items = [*items]
        self.screen = screen

        self.element_type = {
            "hover": [item for item in items if hasattr(item, "hover")],
            "check_click_using_event": [item for item in items if hasattr(item, "check_click_using_event")]
        }

        self.back = background_color

        self.test = pygame.font.Font(get_path("fonts/FiraCode-Regular.ttf"), 24).render("Режим, де ви проти ботів зі штучним", True, (0, 0, 0))

    def sorted_item(self, item):
        for t in self.element_type:
            if hasattr(item, t):
                self.element_type[t].append(item)

    def add_item(self, *items):
        for item in items:
            self.items.append(item)
            self.sorted_item(item)

    def run_loop(self, window, clock: pygame.time.Clock):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for pressable_object in self.element_type["check_click_using_event"]:
                        screen = pressable_object.check_click_using_event(event.pos)
                        if screen: return screen
                elif event.type == pygame.MOUSEMOTION:
                    for hoverable_object in self.element_type["hover"]:
                        hoverable_object.hover(event.pos)
            if self.back: window.fill(self.back)
            for item in self.items:
                item.draw(window)

            # window.blit(self.test, (510, 100))

            pygame.display.update()
            clock.tick(menu_fps)

    def run(self, window, events: list[pygame.event.Event]):
        while True:
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for pressable_object in self.element_type["check_click_using_event"]:
                        screen = pressable_object.check_click_using_event(event.pos)
                        if screen: return screen
                elif event.type == pygame.MOUSEMOTION:
                    for hoverable_object in self.element_type["hover"]:
                        hoverable_object.hover(event.pos)

            for item in self.items:
                item.draw(window)


class FinishLevelMenu(Menu):
    def __init__(self, screen="menu", background_color=(0, 0, 0), *items):
        super().__init__(screen, background_color, *items)


class Menus:
    def __init__(self, current_screen="menu", *menus):
        self.current_screen = current_screen
        self.menus = {menu.screen: menu for menu in menus}
        self.current_menu = self.get_menu()

    def add_submenu(self, *menus):
        for menu in menus:
            self.menus[menu.screen] = menu

    def get_menu(self):
        return self.menus[self.current_screen]

    def change_menu(self, screen):
        if screen == self.current_screen:
            return
        self.current_screen = screen
        self.current_menu = self.get_menu()

    def run_loop(self, window, clock: pygame.time.Clock, screen="menu"):
        self.change_menu(screen)
        while True:
            result = self.current_menu.run_loop(window, clock)
            if result == "menu exit":
                break
            elif result == "game exit":
                pygame.quit()
                exit()
            elif result.startswith("level "):
                return result.replace("level ", "")
            else:
                self.change_menu(result)

    def run(self, window, events: list[pygame.event.Event], screen="menu"):
        self.change_menu(screen)
        result = self.current_menu.run(window, events)
        if result == "menu exit":
            return "exit"
        elif result == "game exit":
            pygame.quit()
            exit()
        elif result.startswith("level "):
            return result.replace("level ", "")
        else:
            self.change_menu(result)


bg_color = background_color


# створення головного меню
main_m = Menu("menu", bg_color)

# створення напису з назвою гри
label_name = Label(366, 30, rect_width=-1,
                   text="Танки 2D",
                   font_family="fonts/PressStart2P-Regular.ttf", font_color=(0, 0, 0), font_size=48)
# створення кнопки-іконки налаштувань
btn_settings_icon = ButtonIcon("images/settings.png", 1140, 10, 50, 50, (30, 255, 30), lambda: "settings")
# створення елементів, що стосуються режимів гри

# режим одного гравця
btn_mode_1 = ButtonText(150, 140, (30, 255, 30), border_radius=10, hover_color=hover_color,
                        text="1 гравець",
                        font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
label_mode_1 = Label(510, 140, rect_width=-1,
                     text="Режим, де ви проти ботів зі штучним\nінтелектом",
                     font_family="fonts/RobotoMono-Regular.ttf", font_color=(0, 0, 0), font_size=24)
# режим двох гравців
btn_mode_2 = ButtonText(150, 370, (30, 255, 30), border_radius=10, hover_color=hover_color,
                        text="2 гравців", on_click=lambda: "level 2",
                        font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
label_mode_2 = Label(510, 370, rect_width=-1,
                     text="Режим, де ви можете грати з другом на\nодному комп’ютері",
                     font_family="fonts/FiraCode-Regular.ttf", font_color=(0, 0, 0), font_size=24)
# режим онлайн гри
btn_mode_online = ButtonText(186, 600, (30, 255, 30), border_radius=10, hover_color=hover_color,
                             text="Онлайн", on_click=lambda: "level online",
                             font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
label_mode_online = Label(510, 600, rect_width=-1,
                          text="Режим, де ви граєте з іншими онлайн.\nНайцікавіший режим :-)",
                          font_family="fonts/FiraCode-Regular.ttf", font_color=(0, 0, 0), font_size=24)

# btn_exit = ButtonText(WIDTH // 2, 580, (30, 255, 30), "Вихід", font_color=(20, 20, 255), font_size=40, border_radius=10,
#                       hover_color=hover_color, center=True)
# btn_exit.onclick(lambda: "game exit")

main_m.add_item(label_name, btn_settings_icon, btn_mode_1, label_mode_1, btn_mode_2, label_mode_2, btn_mode_online, label_mode_online)

settings_m = Menu("settings", bg_color)
# Створення елементів налаштувань
sett_game_info = Label(0, 0, about_game, bg_color=(100, 180, 180), shift_x=20, shift_y=20, line_space=0, width=1000)
btn_back = ButtonText(WIDTH // 2, 530, (30, 255, 30), "Назад", font_color=(20, 20, 255), font_size=40, border_radius=10,
                      hover_color=hover_color, center=True)
btn_back.set_onclick(lambda: "menu")
settings_m.add_item(sett_game_info, btn_back)

pause_m = Menu("pause", None)
# Створення елементів, які будуть відображатися в меню паузи
btn_play = ButtonIcon("images\\play_30_30.png", WIDTH - 30 - 5, 5, 30, 30, on_click=None)
btn_play.set_onclick(lambda: "menu exit")
btn_continue = ButtonText(WIDTH // 2, 100, (30, 255, 30), "Продовжити", font_color=(20, 20, 255), font_size=40,
                          border_radius=10, hover_color=hover_color, center=True)
btn_continue.set_onclick(lambda: "menu exit")
btn_restart = ButtonText(WIDTH // 2, 260, (30, 255, 30), "Почати заново", font_color=(20, 20, 255), font_size=40,
                         border_radius=10, hover_color=hover_color, center=True)
btn_restart.set_onclick(lambda: "menu exit")
btn_menu = ButtonText(WIDTH // 2, 420, (30, 255, 30), "Головне меню", font_color=(20, 20, 255), font_size=40,
                      border_radius=10, hover_color=hover_color, center=True)
btn_menu.set_onclick(lambda: "menu")
pause_m.add_item(btn_play, btn_continue, btn_restart, btn_menu)

menus = Menus("menu", main_m, settings_m, pause_m)