import pygame

# Initialize display information
pygame.init()

info = pygame.display.Info()

# Screen dimensions
WIDTH = info.current_w
HEIGHT = info.current_h

# Board dimensions
ROWS = 8
COLS = 8

# Board size = smaller screen dimension
BOARD_SIZE = min(WIDTH, HEIGHT)

# Size of one square
SQSIZE = BOARD_SIZE // COLS

# Center the board
BOARD_X = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = (HEIGHT - BOARD_SIZE) // 2    