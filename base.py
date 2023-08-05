import pygame
from settings import *

pygame.init()


class Area:
    def __init__(self, x, y, width, height, border_radius=-1, color=None):
        self.rect = pygame.Rect(x, y, width, height)  # прямокутник
        self.border_radius = border_radius

        self.fill_color = background_color
        if color:
            self.fill_color = color

    def color(self, new_color):
        self.fill_color = new_color

    def draw(self, window):
        pygame.draw.rect(window, self.fill_color, self.rect, border_radius=self.border_radius)

    def outline(self, window, frame_color, thickness):  # межа
        pygame.draw.rect(window, frame_color, self.rect, thickness)


class Picture(Area):

    def __init__(self, filename, x, y, width, height, color=None):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=color)
        self.filename = filename
        self.image = pygame.transform.scale(pygame.image.load(filename), (width, height))

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def change_image(self, new_filename):
        self.filename = new_filename
        self.image = pygame.image.load(new_filename)


class Label:
    def __init__(self, x, y, text, width=None, height=None, bg_color=(200, 200, 200), font_family="verdana",
                 font_size=20, font_color=(10, 10, 10), line_space=10, shift_x=0,
                 shift_y=0, border_radius=-1, alpha=255, rect_width=0, center_x=False, center_y=False):
        self.bg_color = bg_color
        self.text = text
        self.font_family = font_family
        self.font_size = font_size
        if font_family.endswith(".ttf"):
            self.font = pygame.font.Font(get_path(font_family), font_size)
        else:
            self.font = pygame.font.SysFont(font_family, font_size)
        self.font_color = font_color
        self.line_space = line_space

        w = 0
        h = 0
        self.rendered_text = []
        for line in text.splitlines():
            rendered_line = self.font.render(line, True, font_color)
            self.rendered_text.append(rendered_line)
            h += rendered_line.get_height()
            if rendered_line.get_width() > w:
                w = rendered_line.get_width()

        self.image = pygame.Surface(
            (width if width else w + shift_x * 2,
             height if height else h + shift_y * 2 + line_space * (len(self.rendered_text) - 1)), pygame.SRCALPHA)
        # self.image.set_alpha(alpha)

        self.rect = self.image.get_rect()
        self.colored_rect = self.image.get_rect()

        pygame.draw.rect(self.image, bg_color, self.colored_rect, rect_width, border_radius=border_radius)

        line_x = shift_x
        line_y = shift_y
        for line in self.rendered_text:
            self.image.blit(line, (line_x, line_y))
            line_y += line.get_height() + self.line_space

        self.width_format = "auto" if not width else "set"
        self.height_format = "auto" if not height else "set"

        if center_x:
            self.rect.x = x - self.image.get_width() // 2
        else:
            self.rect.x = x
        if center_y:
            self.rect.y = y - self.image.get_height() // 2
        else:
            self.rect.y = y

        self.shift_x = shift_x
        self.shift_y = shift_y
        self.border_radius = border_radius
        self.alpha = alpha
        self.rect_width = rect_width
        self.center_x = center_x
        self.center_y = center_y
        self.x = x
        self.y = y

    def set_width(self, width):
        self.rect.width = width
        self.width_format = "set"
        self.render_text()

    def set_height(self, height):
        self.rect.height = height
        self.height_format = "set"
        self.render_text()

    def set_shift_x(self, shift_x):
        self.shift_x = shift_x
        self.render_text()

    def set_shift_y(self, shift_y):
        self.shift_y = shift_y
        self.render_text()

    def set_border_radius(self, border_radius):
        self.border_radius = border_radius
        self.render_text()

    def set_bg_color(self, bg_color):
        self.bg_color = bg_color
        self.render_text()

    def set_text(self, text):
        self.text = text
        self.render_text()

    def set_font_family(self, font_family):
        self.font_family = font_family
        if font_family.endswith(".ttf"):
            self.font = pygame.font.Font(get_path(font_family), self.font_size)
        else:
            self.font = pygame.font.SysFont(font_family, self.font_size)
        self.render_text()

    def set_font_size(self, font_size):
        self.font_size = font_size
        self.font = pygame.font.SysFont(self.font_family, self.font_size)
        self.render_text()

    def set_font_color(self, font_color):
        self.font_color = font_color
        self.render_text()

    def set_line_space(self, line_space):
        self.line_space = line_space
        self.render_text()

    def render_text(self):
        w = 0
        h = 0
        self.rendered_text = []
        for line in self.text.splitlines():
            rendered_line = self.font.render(line, True, self.font_color)
            self.rendered_text.append(rendered_line)
            h += rendered_line.get_height()
            if rendered_line.get_width() > w:
                w = rendered_line.get_width()

        self.image = pygame.Surface(
            (self.rect.width if self.width_format != "auto" else w + self.shift_x * 2,
             self.rect.height if self.height_format != "auto" else h + self.shift_y * 2 + self.line_space * (
                         len(self.rendered_text) - 1)), pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.colored_rect = self.image.get_rect()

        pygame.draw.rect(self.image, self.bg_color, self.colored_rect, self.rect_width,
                         border_radius=self.border_radius)

        x = self.shift_x
        y = self.shift_y
        for line in self.rendered_text:
            self.image.blit(line, (self.rect.x + x, self.rect.y + y))
            y += line.get_height() + self.line_space

        if self.center_x:
            self.rect.x = self.x - self.image.get_width() // 2
        else:
            self.rect.x = self.x
        if self.center_y:
            self.rect.y = self.y - self.image.get_height() // 2
        else:
            self.rect.y = self.y

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Button:
    def __init__(self, x, y,
                 width=None, height=None,
                 bg_color=(255, 255, 255), shift_x=40, shift_y=20, border_radius=-1, hover_color=(200, 200, 200),
                 transition=20,
                 on_click=lambda: print("click"), args=None, kwargs=None, center=False):
        self.rect = pygame.Rect(x, y, width, height)

        self.on_click = on_click
        self.on_click_args = args if args else ()
        self.on_click_kwargs = kwargs if kwargs else {}

    def set_hover_color(self, hover_color):
        self.hover_color = hover_color

    def set_hover_state(self):
        pygame.draw.rect(self.image, self.hover_color, self.colored_rect, border_radius=self.border_radius)
        self.image.blit(self.rendered_text, (self.shift_x, self.shift_y))
        self.state = "hover"

    def set_simple_state(self):
        pygame.draw.rect(self.image, self.bg_color, self.colored_rect, border_radius=self.border_radius)
        self.image.blit(self.rendered_text, (self.shift_x, self.shift_y))
        self.state = "simple"

    def hover(self, pos):
        if self.check_collide(pos):
            if self.state != "hover":
                self.set_hover_state()
        elif self.state != "simple":
            self.set_simple_state()

    def onclick(self, func, *args, **kwargs):
        self.on_click = func
        self.on_click_args = args
        self.on_click_kwargs = kwargs

    def check_collide(self, pos):
        if self.rect.collidepoint(*pos):
            self.set_simple_state()
            return True

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if self.check_collide(pygame.mouse.get_pos()):
                self.on_click(*self.on_click_args, **self.on_click_kwargs)


class ButtonText:
    def __init__(self, x, y, bg_color, text, font_family="verdana", font_size=20, font_color=(10, 10, 10), shift_x=40,
                 shift_y=20, border_radius=-1, hover_color=(200, 200, 200), transition=20,
                 on_click=lambda: print("click"), args=None, kwargs=None, center=False):

        self.on_click = on_click
        self.on_click_args = args if args else ()
        self.on_click_kwargs = kwargs if kwargs else {}

        if font_family.endswith(".ttf"):
            font = pygame.font.Font(get_path(font_family), font_size)
        else:
            font = pygame.font.SysFont(font_family, font_size)
        self.rendered_text = font.render(text, True, font_color)

        self.image = pygame.Surface(
            (self.rendered_text.get_width() + shift_x * 2, self.rendered_text.get_height() + shift_y * 2),
            pygame.SRCALPHA)

        self.rect = self.image.get_rect()
        self.colored_rect = self.image.get_rect()

        pygame.draw.rect(self.image, bg_color, self.colored_rect, border_radius=border_radius)

        self.image.blit(self.rendered_text, (shift_x, shift_y))

        if center:
            self.rect.x = x - self.image.get_width() // 2
            self.rect.y = y - self.image.get_height() // 2
        else:
            self.rect.x = x
            self.rect.y = y

        self.shift_x = shift_x
        self.shift_y = shift_y
        self.border_radius = border_radius
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.state = "simple"
        self.transition = transition
        self.mouse_down = False

    def check_collide(self, pos):
        if self.rect.collidepoint(*pos):
            self.set_simple_state()
            return True

    def set_hover_color(self, hover_color):
        self.hover_color = hover_color

    def hover(self, pos):
        if self.check_collide(pos):
            if self.state != "hover":
                self.set_hover_state()
        elif self.state != "simple":
            self.set_simple_state()

    def set_hover_state(self):
        pygame.draw.rect(self.image, self.hover_color, self.colored_rect, border_radius=self.border_radius)
        self.image.blit(self.rendered_text, (self.shift_x, self.shift_y))
        self.state = "hover"

    def set_simple_state(self):
        pygame.draw.rect(self.image, self.bg_color, self.colored_rect, border_radius=self.border_radius)
        self.image.blit(self.rendered_text, (self.shift_x, self.shift_y))
        self.state = "simple"

    def set_onclick(self, func, *args, **kwargs):
        self.on_click = func
        self.on_click_args = args
        self.on_click_kwargs = kwargs

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if self.check_collide(pygame.mouse.get_pos()):
                self.mouse_down = True
        elif self.mouse_down:
            if self.check_collide(pygame.mouse.get_pos()):
                self.on_click(*self.on_click_args, **self.on_click_kwargs)
            self.mouse_down = False

    def check_click_using_event(self, pos):
        if self.check_collide(pos):
            return self.on_click(*self.on_click_args, **self.on_click_kwargs)

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))


class ButtonIcon(Picture):
    def __init__(self, filename, x, y, width, height, color=None,
                 on_click=lambda: print("click"), args=None, kwargs=None):
        super().__init__(filename, x, y, width, height, color)
        self.on_click = on_click
        self.on_click_args = args if args else ()
        self.on_click_kwargs = kwargs if kwargs else {}
        self.mouse_down = False

    def set_onclick(self, func, *args, **kwargs):
        self.on_click = func
        self.on_click_args = args
        self.on_click_kwargs = kwargs

    def check_click(self):
        if pygame.mouse.get_pressed()[0]:
            if not self.mouse_down:
                if self.check_collide(pygame.mouse.get_pos()):
                    self.mouse_down = True
        elif self.mouse_down:
            if self.check_collide(pygame.mouse.get_pos()):
                self.on_click(*self.on_click_args, **self.on_click_kwargs)
            self.mouse_down = False

    def check_click_using_event(self, pos):
        if self.check_collide(pos):
            return self.on_click(*self.on_click_args, **self.on_click_kwargs)

    def check_collide(self, pos):
        return self.rect.collidepoint(*pos)

    def draw(self, window):
        super().draw(window)


class ProgressBar:
    def __init__(self, x, y, width, height, bg_color):
        pass


class ButtonWithImage:
    def __init__(self, surf, x, y, width, height, color=None, on_click=lambda: None,
                 args=None, kwargs=None):
        pass
