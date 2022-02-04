# константы
import pygame
import os
import random

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_h-50, info.current_h-50

# WIDTH = 600
# HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
timer = 0
curscore = 0
