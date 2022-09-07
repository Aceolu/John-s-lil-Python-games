
#Still figuring this out... Come back later

import pygame
pygame.init()

pygame.display.set_caption("Jong")

#Max framerate
FPS = 60

#RGB Coloring
WHITE = (255,255,255)
BLACK = (0,0,0)

#Window size
WIDTH, HEIGHT = 10, 20
TILE = 45
WINDOW = WIDTH * TILE, HEIGHT * TILE
game_sc = pygame.display.set_mode(WINDOW)

#Building the grid
clock = pygame.time.Clock()
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(WIDTH) for y in range (HEIGHT)]

#Renders the grid each frame?
while True:
    game_sc.fill(pygame.Color('BLACK'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]


    pygame.display.flip()
    clock.tick