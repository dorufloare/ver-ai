import pygame
from lib.sensor import Sensor

def handle_game_controls(keys):
    if keys[pygame.K_q]:
        Sensor.toggle_sensors()

    if keys[pygame.K_ESCAPE] or keys[pygame.K_r]:
        pygame.quit()
    

def handle_user_controls(car, keys):
    if not car.alive:
        return
    if keys[pygame.K_w]:
        car.accelerate()
    if keys[pygame.K_SPACE]:
        car.brake()
    if keys[pygame.K_a]:
        car.turn_left()
    if keys[pygame.K_d]:
        car.turn_right()