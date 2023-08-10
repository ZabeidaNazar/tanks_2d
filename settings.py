import os


PATH = os.path.dirname(os.path.abspath(__file__))


def get_path(*paths):
    return os.path.join(PATH, os.path.normpath(os.path.join(*paths)))


# RES = WIDTH, HEIGHT = 900, 600
RES = WIDTH, HEIGHT = 1200, 800
V_WIDTH = 3000
V_HEIGHT = 2000
BLOCKSIZE = 50
X_BLOCK_COUNT = V_WIDTH // BLOCKSIZE
Y_BLOCK_COUNT = V_HEIGHT // BLOCKSIZE
# print(WIDTH/50, HEIGHT/50)


BULLET_PAUSE = 500
BOT_SPEED = 400  # 300
PLAYER_SPEED = 150

# Menu settings
hover_color = (120, 255, 120)
about_game = "Про гру"
window_title = "Tanks"
background_color = (220, 255, 255)
menu_fps = 30

# colors
LIGHT_VIOLET = (200, 200, 255)
DARC_BLUE = (0, 0, 105)
LIGHT_GREEN = (208, 255, 213)


# CREATE_BONUS = pygame.USEREVENT + 1
# pygame.time.set_timer(CREATE_BONUS, 1000)


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# levels button
COMPLETED_BTN_COLOR = (30, 255, 30)
COMPLETED_BTN_HOVER_COLOR = (120, 255, 120)
UNLOCK_BTN_COLOR = (30, 150, 255)
UNLOCK_BTN_HOVER_COLOR = (50, 170, 255)
LOCK_BTN_COLOR = (176, 176, 176)
LOCK_BTN_HOVER_COLOR = (190, 190, 190)
