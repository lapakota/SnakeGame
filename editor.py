import pygame
from shake import IMAGE, WIDTH, HEIGHT, CELL_SIZE, NOT_BIG_FONT, Portal, Wall

pygame.init()
pygame.display.set_caption('level editor')
surface = pygame.display.set_mode((WIDTH + 300, HEIGHT))

_wall = Wall(0, 0, 'gray55')
_portal = Portal(0, 0, 0, 0, 'white', 'white')
CELLS = []
WALLS = []
PORTALS = []
portals_temp = []
SNAKE_CORDS = ()
is_snake_add = False
is_portal_add = False


def save_level(level_path, walls, portals):
    """Function save walls, portals and snake cords to .txt file"""
    with open(level_path, "w") as file:
        for w in walls:
            print('w' + str(w), file=file)
        for p in portals:
            print('p' + str(p), file=file)
        if is_snake_add:
            print('s' + str(SNAKE_CORDS), file=file)
        print(f'{level_path.split("/")[1]} was saved!')


def is_all_conditions(block, walls, portals_tmp, portals):
    if block[0] < x < block[0] + CELL_SIZE \
            and block[1] < y < block[1] + CELL_SIZE \
            and block not in walls \
            and block not in portals_tmp \
            and block not in [(p[0], p[1]) for p in portals] \
            and block not in [(p[2], p[3]) for p in portals]:
        return True


# adding all cells cords
for row in range(int(HEIGHT / CELL_SIZE)):
    for column in range(int(WIDTH / CELL_SIZE)):
        CELLS.append((column * CELL_SIZE, row * CELL_SIZE))

render_q = NOT_BIG_FONT.render('Press "q" to save level1',
                               0, pygame.Color('green'))
render_w = NOT_BIG_FONT.render('Press "w" to save level2',
                               0, pygame.Color('green'))
render_e = NOT_BIG_FONT.render('Press "e" to save level3',
                               0, pygame.Color('green'))
render_message1 = NOT_BIG_FONT.render('Press left mouse button',
                                      0, pygame.Color('gray55'))
render_message2 = NOT_BIG_FONT.render('to draw walls',
                                      0, pygame.Color('gray55'))
render_message3 = NOT_BIG_FONT.render('Press right mouse button',
                                      0, pygame.Color('red'))
render_message4 = NOT_BIG_FONT.render('to erase walls',
                                      0, pygame.Color('red'))
render_message5 = NOT_BIG_FONT.render('Press "d" keyboard button',
                                      0, pygame.Color('white'))
render_message6 = NOT_BIG_FONT.render('to draw portals',
                                      0, pygame.Color('white'))
render_message7 = NOT_BIG_FONT.render('Press "s" keyboard button',
                                      0, pygame.Color('orange'))
render_message8 = NOT_BIG_FONT.render('to draw snake position',
                                      0, pygame.Color('orange'))
render_message9 = NOT_BIG_FONT.render('Press space to erase all',
                                      0, pygame.Color('red'))
render_message10 = NOT_BIG_FONT.render(':3',
                                       0, pygame.Color('red'))

while True:
    surface.blit(IMAGE, (0, 0))
    # draw snake position
    if is_snake_add:
        pygame.draw.rect(surface, pygame.Color('orange'),
                         (SNAKE_CORDS[0], SNAKE_CORDS[1], CELL_SIZE, CELL_SIZE))
    for wall in WALLS:
        pygame.draw.rect(surface, pygame.Color(_wall.color),
                         (wall[0], wall[1], CELL_SIZE, CELL_SIZE))
    for portal in PORTALS:
        pygame.draw.rect(surface, pygame.Color(_portal.f_color),
                         (portal[0], portal[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, pygame.Color(_portal.s_color),
                         (portal[2], portal[3], CELL_SIZE, CELL_SIZE))
    # draw single portal that's don't have partner
    if is_portal_add:
        pygame.draw.rect(surface, pygame.Color('aquamarine'),
                         (portals_temp[0][0], portals_temp[0][1], CELL_SIZE, CELL_SIZE))

    surface.blit(render_q, (WIDTH + 10, 5))
    surface.blit(render_w, (WIDTH + 10, 30))
    surface.blit(render_e, (WIDTH + 10, 55))
    surface.blit(render_message1, (WIDTH + 10, 100))
    surface.blit(render_message2, (WIDTH + 10, 125))
    surface.blit(render_message3, (WIDTH + 10, 160))
    surface.blit(render_message4, (WIDTH + 10, 185))
    surface.blit(render_message5, (WIDTH + 10, 220))
    surface.blit(render_message6, (WIDTH + 10, 245))
    surface.blit(render_message7, (WIDTH + 10, 280))
    surface.blit(render_message8, (WIDTH + 10, 305))
    surface.blit(render_message9, (WIDTH + 10, 350))
    surface.blit(render_message10, (WIDTH + 50, 750))

    pygame.display.flip()
    key = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # left mouse button
        if mouse[0]:
            for cell in CELLS:
                if is_all_conditions(cell, WALLS, portals_temp, PORTALS):
                    WALLS.append((cell[0], cell[1]))
        # right mouse button
        if mouse[2]:
            for cell in CELLS:
                if cell[0] < x < cell[0] + CELL_SIZE \
                        and cell[1] < y < cell[1] + CELL_SIZE:
                    if cell in WALLS:
                        WALLS.remove((cell[0], cell[1]))
                    for portal in PORTALS:
                        if cell[0] in portal and cell[1] in portal:
                            PORTALS.remove(portal)
                    if cell == SNAKE_CORDS:
                        is_snake_add = False
                        SNAKE_CORDS = ()
        if key[pygame.K_d]:
            for cell in CELLS:
                if is_all_conditions(cell, WALLS, portals_temp, PORTALS):
                    if is_portal_add:
                        portals_temp.append((cell[0], cell[1]))
                        PORTALS.append((portals_temp[0][0], portals_temp[0][1],
                                        portals_temp[1][0], portals_temp[1][1]))
                        portals_temp.clear()
                        is_portal_add = False
                    else:
                        portals_temp.append((cell[0], cell[1]))
                        is_portal_add = True
        if key[pygame.K_s]:
            for cell in CELLS:
                if is_all_conditions(cell, WALLS, portals_temp, PORTALS):
                    SNAKE_CORDS = (cell[0], cell[1])
                    is_snake_add = True
        if event.type == pygame.QUIT:
            exit()
        if key[pygame.K_SPACE]:
            WALLS.clear()
            PORTALS.clear()
            portals_temp.clear()
            SNAKE_CORDS = ()
            is_snake_add = False
            is_portal_add = False
        if key[pygame.K_q]:
            save_level('levels/level1.txt', WALLS, PORTALS)
        if key[pygame.K_w]:
            save_level('levels/level2.txt', WALLS, PORTALS)
        if key[pygame.K_e]:
            save_level('levels/level3.txt', WALLS, PORTALS)
    pygame.display.update()
