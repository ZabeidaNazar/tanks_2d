import pygame
from settings import *
from base import ButtonText, ButtonIcon, Label, Area, Picture, TransparentRect, ImageOfDisplay


class Menu:
    def __init__(self, screen="menu", background_color=(0, 0, 0), *items):
        self.items = [*items]
        self.screen = screen

        self.element_type = {
            "hover": [item for item in items if hasattr(item, "hover")],
            "check_click_using_event": [item for item in items if hasattr(item, "check_click_using_event")],
            "activated": [item for item in items if hasattr(item, "activated")],
        }

        self.back = background_color

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

    def draw(self, window):
        for item in self.items:
            item.draw(window)

    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for pressable_object in self.element_type["check_click_using_event"]:
                screen = pressable_object.check_click_using_event(event.pos)
                if screen:
                    if pressable_object in self.element_type["activated"]:
                        for activated_object in self.element_type["activated"]:
                            if activated_object is pressable_object:
                                continue
                            activated_object.dis_activated()
                        pressable_object.activated()
                        return screen[1]
                    return screen
        elif event.type == pygame.MOUSEMOTION:
            for hoverable_object in self.element_type["hover"]:
                hoverable_object.hover(event.pos)


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
btn_mode_2 = ButtonText(150, 302, (30, 255, 30), border_radius=10, hover_color=hover_color,
                        text="2 гравців", on_click=lambda: "level 2",
                        font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
label_mode_2 = Label(510, 302, rect_width=-1,
                     text="Режим, де ви можете грати з другом на\nодному комп’ютері",
                     font_family="fonts/FiraCode-Regular.ttf", font_color=(0, 0, 0), font_size=24)
# режим онлайн гри
btn_mode_online = ButtonText(186, 464, (30, 255, 30), border_radius=10, hover_color=hover_color,
                             text="Онлайн", on_click=lambda: "level online",
                             font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
label_mode_online = Label(510, 464, rect_width=-1,
                          text="Режим, де ви граєте з іншими онлайн.\nНайцікавіший режим :-)",
                          font_family="fonts/FiraCode-Regular.ttf", font_color=(0, 0, 0), font_size=24)
# режим редактора рівнів
btn_mode_editor = ButtonText(162, 626, (30, 255, 30), border_radius=10, hover_color=hover_color,
                             text="Редактор", on_click=lambda: "mode editor",
                             font_family="fonts/FiraCode-Regular.ttf", font_color=(20, 20, 255), font_size=40)
label_mode_editor = Label(510, 626, rect_width=-1,
                          text="Режим, де ви можете створювати власні\nрівні",
                          font_family="fonts/FiraCode-Regular.ttf", font_color=(0, 0, 0), font_size=24)

# btn_exit = ButtonText(WIDTH // 2, 580, (30, 255, 30), "Вихід", font_color=(20, 20, 255), font_size=40, border_radius=10,
#                       hover_color=hover_color, center=True)
# btn_exit.onclick(lambda: "game exit")

main_m.add_item(label_name, btn_settings_icon,
                btn_mode_1, label_mode_1,
                btn_mode_2, label_mode_2,
                btn_mode_online, label_mode_online,
                btn_mode_editor, label_mode_editor)

settings_m = Menu("settings", bg_color)
# Створення елементів налаштувань
sett_game_info = Label(0, 0, about_game, bg_color=(100, 180, 180), shift_x=20, shift_y=20, line_space=0, width=1000)
btn_back = ButtonText(WIDTH // 2, 530, (30, 255, 30), "Назад", font_color=(20, 20, 255), font_size=40, border_radius=10,
                      hover_color=hover_color, center_x=True)
btn_back.set_onclick(lambda: "menu")
settings_m.add_item(sett_game_info, btn_back)

menus = Menus("menu", main_m, settings_m)
