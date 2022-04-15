from random import randint
import pygame
from sys import exit
import tetrisfunctions


# Left arrow key -> move left
# Right arrow key -> move right
# Down arrowy key -> move down faster
# Spacebar -> rotate

def main():
    pygame.font.init()
    pygame.display.set_caption("Tetris")

    NUMBER_OF_TILES_X = 10
    NUMBER_OF_TILES_Y = 20
    TILE_SIZE = 30
    FPS = 60
    BACKGROUND_COLOR = (0, 0, 0)
    SCREEN_FRAME_COLOR = (0,51,102)
    TILES_COLORS = [(0, 204, 255), (0, 0, 255), (255, 0, 0), (51, 204, 51), (255, 255, 0), (255, 0, 255)]
    FONT = pygame.font.SysFont('consolas', 7*TILE_SIZE//10, True)
    width, height = (NUMBER_OF_TILES_X + 2) * TILE_SIZE, (NUMBER_OF_TILES_Y + 2) * TILE_SIZE
    bottom_border = pygame.Rect(0, height - TILE_SIZE, width, TILE_SIZE)
    top_border = pygame.Rect(0, 0, width, TILE_SIZE)
    left_border = pygame.Rect(0, 0, TILE_SIZE, height)
    right_border = pygame.Rect(width - TILE_SIZE, 0, TILE_SIZE, height)
    border_tiles = []
    floor_tiles = []
    floor_tiles_colors = dict()
    score = 0
    for y in range(0, height, TILE_SIZE):
        for x in range(0, width, TILE_SIZE):
            if y == 0 or y == height - TILE_SIZE:
                border_tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            elif x == 0 or x == width - TILE_SIZE:
                border_tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))

    WIN = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    run = True
    figure = tetrisfunctions.createFigure(TILE_SIZE, NUMBER_OF_TILES_X, NUMBER_OF_TILES_Y, randint(0,6), randint(1,4), randint(0,4))
    figure_tiles = tetrisfunctions.update_tiles(figure, TILE_SIZE)
    tile_color = TILES_COLORS[randint(0, len(TILES_COLORS)-1)]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                tetrisfunctions.handle_figure_movement(figure, event.key, floor_tiles, bottom_border, left_border, right_border, TILE_SIZE)
                figure_tiles = tetrisfunctions.update_tiles(figure, TILE_SIZE)
        if tetrisfunctions.done_falling(figure_tiles, bottom_border, floor_tiles):
            figure.set_moving(False)
            score += 5
            for tile in figure_tiles:
                floor_tiles.append(tile)
                floor_tiles_colors[(tile.x, tile.y)] = tile_color
            tile_color = TILES_COLORS[randint(0, len(TILES_COLORS)-1)]
            figure = tetrisfunctions.createFigure(TILE_SIZE, NUMBER_OF_TILES_X, NUMBER_OF_TILES_Y, randint(0,6), randint(1,4), randint(0,6))
            figure_tiles = tetrisfunctions.update_tiles(figure, TILE_SIZE)
            score = tetrisfunctions.handle_line_fill(floor_tiles, TILE_SIZE, NUMBER_OF_TILES_X, NUMBER_OF_TILES_Y, floor_tiles_colors, score)
        tetrisfunctions.update_window(figure_tiles, WIN, BACKGROUND_COLOR, SCREEN_FRAME_COLOR, top_border, floor_tiles, tile_color, left_border, right_border, floor_tiles_colors, FONT, score, border_tiles, TILE_SIZE)
        run = tetrisfunctions.check_end_game(floor_tiles, top_border)
        figure.move_down()
        figure_tiles = tetrisfunctions.update_tiles(figure, TILE_SIZE)
    if tetrisfunctions.ending_screen(WIN, BACKGROUND_COLOR, SCREEN_FRAME_COLOR, score, FONT, width, height, border_tiles, TILE_SIZE):
        main()

if __name__ == "__main__":
    main()