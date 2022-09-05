
#Still figuring this out...


import pygame

WIDTH, HEIGHT = 10, 20

TILE = 45

WINDOW = WIDTH * TILE, HEIGHT * TILE
FPS = 60

pygame.init()
game_sc = pygame.display.set_mode(WINDOW)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range (HEIGHT)]

while True:
    game_sc.fill(pygame.Color('black'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]


    pygame.display.flip()
    clock.tick