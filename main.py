import pygame
import threading
from menu import menus
import menu
from loading_screen import LoadingScreen
from settings import *
from modes.mode_1_player.mode import Mode as Mode1

pygame.init()
pygame.display.set_caption(window_title)


class Game:
    def __init__(self):
        self.main_screen = pygame.display.set_mode(RES)
        self.time = pygame.time.Clock()
        self.playing = True

        self.current_mode = None
        self.loaded_modes = {}

        menu.btn_mode_1.set_onclick(self.change_mode, "mode 1")

        self.loading_screen = LoadingScreen(self)
        # self.level = Levels_simple.Level(self.time)

    def run_loading_screen(self):
        pygame.display.set_caption(f"{window_title} - Loading...")
        threading.Thread(name="Loading", target=self.loading_screen.run, daemon=True).start()

    def stop_loading_screen(self):
        self.loading_screen.stop()

    def change_mode(self, name):
        if name not in self.loaded_modes:
            self.run_loading_screen()
            mode = Mode1(self)
            self.loaded_modes[name] = mode
            self.current_mode = mode
            self.stop_loading_screen()
        else:
            self.current_mode = self.loaded_modes[name]
        return "menu exit"

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def run(self):
        # main_menu(self.main_screen, self.time, "menu")
        menus.run_loop(self.main_screen, self.time)
        while self.playing:
            self.get_event()

            self.current_mode.run()
               
            pygame.display.flip()
            pygame.display.set_caption(f"{window_title}  fps:  {str(self.time.get_fps())}")
            self.time.tick(30)     # 10


if __name__ == "__main__":
    game = Game()
    game.run()
