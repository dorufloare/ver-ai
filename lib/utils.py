import pygame
from lib.globals import *

def initialize_pygame():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("F1 Simulator")
    
    map_image = pygame.image.load(MAP_IMAGE_PATHS[1]).convert_alpha()
    map_image = pygame.transform.scale(map_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

    return window, map_image

