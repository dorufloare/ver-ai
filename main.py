import pygame
from lib.globals import *
from lib.controls import *
from lib.car import Car
from lib.utils import *

def main():
    window, game_map = initialize_pygame()
    car = Car(CAR_START_X, CAR_START_Y)
    cars = pygame.sprite.Group()
    cars.add(car)

    clock = pygame.time.Clock()
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()

        handle_user_controls(car, keys)
        handle_game_controls(keys);
   
        cars.update(game_map)

        window.blit(game_map, (0, 0))
        cars.draw(window)
      
        if (DRAW_SENSORS):
            car.draw_sensors(window)

        pygame.display.flip()

        clock.tick_busy_loop(60)

    pygame.quit()


if __name__ == "__main__":
    main()
