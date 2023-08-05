import pygame
import threading
from settings import RES, window_title, BLACK, WIDTH, HEIGHT
from base import Label


class LoadingScreen:
    def __init__(self, game):
        self.game = game
        self.main_screen = self.game.main_screen
        self.time = self.game.time
        self.is_run = True

        self.loading_label = Label(WIDTH / 2, HEIGHT / 2.5, center_x=True, rect_width=-1,
                                   text="Завантаження...",
                                   font_color=(255, 255, 255))

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_run = False

    def run(self):
        # pygame.display.set_caption(f"{window_title} - Loading...")
        self.is_run = True
        self.main_screen.fill(BLACK)
        pygame.display.flip()
        while self.is_run:
            self.get_event()
            self.main_screen.fill(BLACK)

            to_update_rect = self.main_screen.blit(self.loading_label.image, self.loading_label.rect)

            pygame.display.update(to_update_rect)
            # pygame.display.set_caption(f"{window_title} - Loading...")
            self.time.tick(30)

    def stop(self):
        self.is_run = False


if __name__ == "__main__":
    class Test:
        def __init__(self):
            self.main_screen = pygame.display.set_mode(RES)
            self.time = pygame.time.Clock()
    loading_screen = LoadingScreen(Test())
    loading_screen.run()
