from time import sleep


game_map = [
    [2, 2, 2, 2, 2, 2, 2],
    [2, 5, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 2, 2, 2],
    [2, 0, 0, 0, 0, 0, 2],
    [2, 0, 0, 0, 0, 0, 2],
    [2, 1, 0, 0, 0, 0, 2],
    [2, 1, 0, 0, 1, 7, 2],
]

game_map = [
    [2, 2, 2, 2, 2],
    [2, 0, 0, 5, 2],
    [2, 7, 2, 0, 2],
    [2, 0, 0, 0, 2],
    [2, 2, 2, 2, 2],
]

for row in game_map:
    try:
        our_x = row.index(5)
        our_y = game_map.index(row)
    except:
        pass

    try:
        enemy_x = row.index(7)
        enemy_y = game_map.index(row)
    except:
        pass

print(f"Our: {our_x=}, {our_y=}   \nEnemy: {enemy_x=}, {enemy_y=} ")

def my_pprint():
    for row in game_map:
        print(row)
    print("\n")

def choose(our_x, our_y):
    global game_map

    pathes = []


    if game_map[our_y][our_x - 1] != 2 and game_map[our_y][our_x - 1] != 8:
        pathes.append((our_x-1, our_y, None))
    elif game_map[our_y][our_x + 1] != 2 and game_map[our_y][our_x + 1] != 8:
        pathes.append((our_x+1, our_y, None))
    elif game_map[our_y + 1][our_x] != 2 and game_map[our_y + 1][our_x] != 8:
        pathes.append((our_x, our_y+1, None))
    elif game_map[our_y - 1][our_x] != 2 and game_map[our_y - 1][our_x] != 8:
        pathes.append((our_x, our_y-1, None))

    return pathes



def search_path(our_x, our_y):
    global game_map

    for starts in choose(our_x, our_y):
        our_x, our_y, _ = starts


        if game_map[our_y][our_x - 1] != 2 and game_map[our_y][our_x - 1] != 8:
            if game_map[our_y][our_x - 1] == 7:
                return 7
            else:
                game_map[our_y][our_x - 1] = 8
            our_x -= 1 
        elif game_map[our_y][our_x + 1] != 2 and game_map[our_y][our_x + 1] != 8:
            if game_map[our_y][our_x + 1] == 7:
                return 7
            else:
                game_map[our_y][our_x + 1] = 8
            our_x += 1 
        elif game_map[our_y + 1][our_x] != 2 and game_map[our_y + 1][our_x] != 8:
            if game_map[our_y + 1][our_x] == 7:
                return 7
            else:
                game_map[our_y + 1][our_x] = 8
            our_y += 1 
        elif game_map[our_y - 1][our_x] != 2 and game_map[our_y - 1][our_x] != 8:
            if game_map[our_y - 1][our_x] == 7:
                return 7
            else:
                game_map[our_y - 1][our_x] = 8
            our_y -= 1 
    my_pprint() 
        



while True:
    
    if search_path(our_x=our_x, our_y=our_y) == 7:
        break

    sleep(3)


# my_pprint()