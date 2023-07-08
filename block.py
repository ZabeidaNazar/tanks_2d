import pygame
from settings import *
from game_map import *


class Block(pygame.sprite.Sprite):
    def __init__(self, groups, type_block, image, x, y, color=(0, 100, 0, 0.5)):
        super().__init__(groups) if groups is not None else super().__init__()
        if not image:
            self.image = pygame.Surface((BLOCKSIZE, BLOCKSIZE))
            if len(color) == 3:
                self.image.fill(color)
            elif len(color) == 4:
                self.image.fill(color[:-1])
                self.image.set_alpha(color[-1])
        else:
            self.image = pygame.transform.scale(pygame.image.load(f"{PATH}/{image}").convert_alpha(), (BLOCKSIZE, BLOCKSIZE))
        self.rect = self.image.get_rect()
        self.rect.x = BLOCKSIZE * x
        self.rect.y = BLOCKSIZE * y
        self.old_rect = self.rect.copy()

        self.x = x
        self.y = y

        self.type_block = type_block

    # def __getstate__(self):
    #     attributes = self.__dict__.copy()
    #     attributes["image"] = pygame.image.tostring(self.image, "RGBA")
    #     return attributes
    
    # def __setstate__(self, state):
    #     surface_str = state
    #     self.image = pygame.image.fromstring(surface_str, "RGBA")


    def draw():
        pass

    def __str__(self):
        return f"{self.x=}, {self.y=}"
    
class BlockPicture(Block):
        def __init__(self, type_block, image, x, y):
            super().__init__(type_block, image, x, y)

            self.image = pygame.transform.scale(pygame.image.load(f"{PATH}/{image}"), (BLOCKSIZE, BLOCKSIZE))
            self.rect = self.image.get_rect()





    # def parse_map(self):
    #     for row in game_map:
    #         for item in row:
    #             if item == 0:
    #                 self.
    #             elif item == 1:
    #             elif item == 2:



def get_blocks(groups):
    # if load:
    #     import pickle
    #     with open(f"{PATH}/data/map.my_map", "rb") as file:
    #         pickle.load(file)
    #     return
    blocks = []
    x = 0
    y = 0
    for row in game_map:
        for item in row:                
            if item == 1:
                blocks.append(  Block(groups, 1, "images/wall.png", x, y)  )
            elif item == 2:
                blocks.append(  Block(groups, 2, "images/wall1.png", x, y)  )
            elif item == 0:
                # blocks.append(  Block(0, "", x, y)  ) 
                pass
            else:
                print(f"Incorrect value: '{item}'")
            x += 1

        x = 0;  y += 1
    
    # if save:
    #     import pickle
    #     with open(f"{PATH}/data/map.my_map", "wb") as file:
    #         pickle.dump(blocks, file)

    return blocks


# get_blocks(True, True)
