import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, group, image_path, x, y, wight, height, speed_x, speed_y, move=False):
        super().__init__(group)
        self.window = pygame.display.get_surface()
        self.image = pygame.transform.scale(pygame.image.load(image_path), (wight, height)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.direction = [1, 1]

        self.move = move

    def move_x(self):
        self.rect.x += self.speed_x * self.direction[0]

    def move_y(self):
        self.rect.y += self.speed_y * self.direction[1]

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction[0] = -1
            self.move_x()
        if keys[pygame.K_s]:
            self.direction[1] = 1
            self.move_y()
        if keys[pygame.K_d]:
            self.direction[0] = 1
            self.move_x()
        if keys[pygame.K_w]:
            self.direction[1] = -1
            self.move_y()

    def draw(self):
        self.window.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        if self.move: self.input()
        # self.draw()
