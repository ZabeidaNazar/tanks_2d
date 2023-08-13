import pygame
import game_map
from settings import V_WIDTH, V_HEIGHT, get_path


class CameraGroup(pygame.sprite.Group):
    def __init__(self, target="player"):
        super().__init__()
        self.window = pygame.display.get_surface()
        self.half_width = self.window.get_width() // 2
        self.half_height = self.window.get_height() // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.transform.scale(pygame.image.load(get_path('images/background.png')).convert_alpha(), (V_WIDTH, V_HEIGHT))
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

        self.keyboard_speed = 3

        if target == "keyboard":
            def inner(self):
                self.keyboard_offset()
                self.custom_draw()
            # __class__.drawing = inner
            setattr(self, "drawing", inner)
        else:
            def inner(self, player):
                self.player_offset(player)
                self.custom_draw()
            # __class__.drawing = inner
            setattr(self, "drawing", inner)

    def set_keyboard_speed(self, speed):
        self.keyboard_speed = speed

    def keyboard_offset(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.offset.y -= self.keyboard_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.offset.y += self.keyboard_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.offset.x -= self.keyboard_speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.offset.x += self.keyboard_speed

    def player_offset(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

    def custom_draw(self):

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.window.blit(self.floor_surf, floor_offset_pos)

        # for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.z_index):
            offset_pos = sprite.rect.topleft - self.offset
            self.window.blit(sprite.image, offset_pos)

            # rect = sprite.rect.move(-self.offset.x, -self.offset.y)
            # pygame.draw.rect(self.window, (255, 0, 0), rect, 1)
            # rect = sprite.old_rect.move(-self.offset.x, -self.offset.y)
            # pygame.draw.rect(self.window, (255, 0, 0), rect, 1)

            # pygame.draw.rect(self.window, (255, 0, 0), sprite.rect, 3)
            # pygame.draw.rect(self.window, (255, 0, 0), sprite.old_rect, 3)
