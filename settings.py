import os


PATH = os.path.abspath(__file__) + "\.."

# RES = WIDTH, HEIGHT = 900, 600
RES = WIDTH, HEIGHT = 1200, 800
BLOCKSIZE = 50
# print(WIDTH/50, HEIGHT/50)


BULLET_PAUSE = 800
BOT_SPEED = 400  # 300
PLAYER_SPEED = 150


# CREATE_BONUS = pygame.USEREVENT + 1
# pygame.time.set_timer(CREATE_BONUS, 1000)


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)