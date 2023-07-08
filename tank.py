import pygame
from collections import deque
# from block import *
from settings import *
from game_map import *
from bullet import *

pygame.init()

class Tank(pygame.sprite.Sprite):
    def __init__(self, game, groups, filename, x, y, speed, type_bullet_pause=True, bullet_count=None,
                 bullet_pause=BULLET_PAUSE):
        super().__init__(groups) if groups is not None else super().__init__()
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(f"{PATH}/{filename}").convert_alpha(), (BLOCKSIZE, BLOCKSIZE))
        self.image_kill = pygame.transform.scale(pygame.image.load(f"{PATH}/images/kill.png").convert_alpha(), (BLOCKSIZE, BLOCKSIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x * BLOCKSIZE
        self.rect.y = y * BLOCKSIZE
        self.old_rect = self.rect.copy()
        self.speed = speed
        self.angle = 0
        self.bullets = []
        if bullet_count:
            for b_c in range(bullet_count):
                self.bullets.append(Bullet(None, self, f"{PATH}/images/bullet.png", 10))
            self.bullets_flight = []

        self.bullet_pause = bullet_pause
        self.can_do_bullet = True
        self.attack_time = None

        if type_bullet_pause:
            self.__class__.get_bullet = __class__.get_bullet_with_pause
        else:
            self.__class__.get_bullet = __class__.get_bullet_without_pause



    def rotate(self, angle):
        if angle != self.angle:
            self.rotate_angle(360 - self.angle + angle)
            self.angle = angle

    def rotate_angle(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)


    def get_bullet_with_pause(self):
        if self.can_do_bullet:
            if self.bullets:
                b = self.bullets.pop()
                b.update_cord()
                self.bullets_flight.append(b)

                b.add(self.groups())
                self.can_do_bullet = False
                self.attack_time = pygame.time.get_ticks()

    def check_can_do_bullet(self):
        if self.can_do_bullet:
            return
        if pygame.time.get_ticks() - self.attack_time >= self.bullet_pause:
            self.can_do_bullet = True

    def get_bullet_without_pause(self):
        if self.bullets:
            b = self.bullets.pop()
            b.update_cord()
            self.bullets_flight.append(b)

            b.add(self.groups())


    def draw(self):
        for bullet in self.bullets:
            bullet.draw()
        self.game.main_screen.blit(self.image, (self.rect.x, self.rect.y))

    def draw_count(self):
        for bullet in self.bullets_flight:
            bullet.draw_count()
        self.game.main_screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def check_collide(self, enemies):
        enemies_rect = []
        for e in enemies:
            enemies_rect.append(e.rect)
        n = self.rect.collidelist(enemies)
        if n != -1:
            n = enemies.pop(n)
            n.remove(n.groups())
            self.game.is_kill = True; self.old_rect = self.rect.copy()
            self.draw_count = self.draw4

    def draw2(self):
        for bullet in self.bullets:
            bullet.draw()
        self.game.main_screen.blit(self.image, (self.rect.x, self.rect.y)); pygame.draw.rect(self.game.main_screen, (255, 0, 0), self.rect, 1)

    def draw3(self):
        for bullet in self.bullets:
            bullet.draw()

    def draw4(self):
        for bullet in self.bullets_flight:
            bullet.draw_count()
        self.game.main_screen.blit(self.image, (self.rect.x, self.rect.y))
        self.game.main_screen.blit(self.image_kill, (self.rect.x, self.rect.y))

    def update(self):
        self.check_can_do_bullet()
        


class Tank_Control(Tank):
    def __init__(self, game, groups, obstracles_group, filename, x, y, speed, type_bullet_pause=True, bullet_count=None,
                 bullet_pause=BULLET_PAUSE):
        super().__init__(game, groups, filename, x, y, speed, type_bullet_pause, bullet_count, bullet_pause)
        self.obstracles_group = obstracles_group

        self.collision_x()
        self.collision_y()

    def collision_x(self):
        for sprite in pygame.sprite.spritecollide(self, self.obstracles_group, False):
            if self.rect.right > sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                self.rect.right = sprite.rect.left
            elif self.rect.left < sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                self.rect.left = sprite.rect.right

    def collision_y(self):
        for sprite in pygame.sprite.spritecollide(self, self.obstracles_group, False):
            if self.rect.bottom > sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                self.rect.bottom = sprite.rect.top
            elif self.rect.top < sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                self.rect.top = sprite.rect.bottom

    def walls_collision(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > V_WIDTH:
            self.rect.right = V_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > V_HEIGHT:
            self.rect.bottom = V_HEIGHT

    def go(self):
        self.old_rect = self.rect.copy()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.rect.y += self.speed
            self.rotate(180)
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            self.rect.y -= self.speed
            self.rotate(0)
        self.collision_y()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            self.rect.x += self.speed
            self.rotate(270)
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            self.rect.x -= self.speed
            self.rotate(90)
        self.collision_x()
        if keys[pygame.K_TAB] or keys[pygame.K_RCTRL]:
            self.get_bullet()

    def update(self):
        super().update()
        self.go()
        self.walls_collision()


class TankAutoControl(Tank):
    def __init__(self, game, groups, filename, x, y, speed, type_bullet_pause=False, bullet_count=None, bullet_pause=BULLET_PAUSE):
        super().__init__(game, groups, filename, x, y, speed, type_bullet_pause, bullet_count, bullet_pause)
        self.ways = (-1, 0), (0, -1), (1, 0), (0, 1)
        self.path = None
        self.enemy_x = 0
        self.our_x = 0
        self.enemy_y = 0
        self.our_y = 0

    def draw_point(self):
        pygame.draw.rect(self.game.main_screen, (255, 0, 0), pygame.Rect(self.enemy_x*BLOCKSIZE, self.enemy_y*BLOCKSIZE, BLOCKSIZE, BLOCKSIZE), 2, 20)

    def draw_path(self):
        if not self.path:
            return
        

        for cord in self.path:
            x, y = cord
            pygame.draw.rect(self.game.main_screen, (0, 255, 0), pygame.Rect(x*BLOCKSIZE+BLOCKSIZE//4, y*BLOCKSIZE+BLOCKSIZE//4, BLOCKSIZE//2, BLOCKSIZE//2), 2, 50)


    def listen_key(self, enemy):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_g]:
            self.get_cord(enemy)
        if keys[pygame.K_r]:
            self.get_cord(enemy)
            self.alogoritm_A()
        if keys[pygame.K_q]:
            print(self.path)

    def get_cord(self, enemy: Tank):
        self.enemy_x = enemy.rect.x // BLOCKSIZE
        self.enemy_y = enemy.rect.y // BLOCKSIZE
        self.enemy = (self.enemy_x , self.enemy_y)
        # print(self.enemy_x, self.enemy_y)

        self.our_x = self.rect.x // BLOCKSIZE
        self.our_y = self.rect.y // BLOCKSIZE



    def get_next_node(self, x, y):
        next_nodes = []
        for dx, dy in self.ways:
            if self.check_next_node(x+dx, y+dy):
                next_nodes.append((x+dx, y+dy))
        return next_nodes

    def check_next_node(self, x, y):
        if 0 > x or x > X_BLOCK_COUNT - 1 or 0 > y or y > Y_BLOCK_COUNT - 1:
            return False
        return 0 <= x < len(game_map[y]) and 0 <= y < len(game_map) and not game_map[y][x]
        # return 0 <= x < len(game_map[y]) and 0 <= y < len(game_map) and (not game_map[y][x] or game_map[y][x] == 1)




    def alogoritm_A(self):
        start = (self.our_x, self.our_y)
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == self.enemy:
                break

            next_nodes = self.get_next_node(*cur_node)
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        if self.enemy not in visited:
            return
        # path = deque([])
        path = []
        path.append(self.enemy)
        cur_node = self.enemy
        while cur_node != start:
            cur_node = visited[cur_node]
            path.append(cur_node)
        if len(path) > 2:
            self.path = deque(path[-2::-1])



    def move(self, enemy):
        if self.path:
            if len(self.path) == 1:
                x, y = self.path.popleft()
                our_x = self.rect.x // BLOCKSIZE
                our_y = self.rect.y // BLOCKSIZE
                x = x - our_x
                y = y - our_y
                if x == -1:
                    self.rotate(90)
                elif x == 1:
                    self.rotate(270)
                elif y == -1:
                    self.rotate(0)
                elif y == 1:
                    self.rotate(180) 
            else:
                self.old_rect = self.rect.copy()
                x, y = self.path.popleft()
                our_x = self.rect.x // BLOCKSIZE
                our_y = self.rect.y // BLOCKSIZE
                x = x - our_x 
                y = y - our_y 
                if x == -1:
                    self.rotate(90)
                    self.rect.x -= self.speed
                elif x == 1:
                    self.rect.x += self.speed
                    self.rotate(270)
                elif y == -1:
                    self.rect.y -= self.speed
                    self.rotate(0)
                elif y == 1:
                    self.rect.y += self.speed
                    self.rotate(180)
            # print(x, y)
            if self.our_x == self.enemy_x or self.our_y == self.enemy_y:
                self.get_bullet()
        else:
            pass
        self.get_cord(enemy)
        self.alogoritm_A()

        # if self.our_x == self.enemy_x or self.our_y == self.enemy_y:
        #     self.get_bullet()

        




    # def search_path(self):
    #     # for row in game_map:
    #     if game_map[self.our_y][self.our_x - 1] == 0:
    #         self.rect.x -= self.speed
    #         self.rotate(90)
    #     elif game_map[self.our_y][self.our_x + 1] == 0:
    #         self.rect.x += self.speed
    #         self.rotate(270)
    #     elif game_map[self.our_y + 1][self.our_x] == 0:
    #         self.rect.y -= self.speed
    #         self.rotate(0)
    #     elif game_map[self.our_y - 1][self.our_x] == 0:
    #         self.rect.y += self.speed
    #         self.rotate(180)
    #         # for column in row:
    #         #     pass
