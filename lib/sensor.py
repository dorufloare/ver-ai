from lib.globals import *
import math
import pygame

class Sensor:
    draw_sensors = True
    def __init__(self, x, y, angle, sensivity=SENSOR_SENSIVITY):
        self.start_x = x
        self.end_x = x
        self.start_y = y 
        self.end_y = y  
        self.angle = angle
        self.sensivity = sensivity

    @classmethod
    def get_distance(cls, x1, y1, x2, y2):
        delta_x = x1 - x2
        delta_y = y1 - y2
        return int(math.sqrt(delta_x * delta_x + delta_y * delta_y))

    @classmethod
    def toggle_sensors(cls):
        Sensor.draw_sensors = not Sensor.draw_sensors

    def get_data(self, game_map, car_angle):
        length = 0
        angle = self.angle + car_angle

        self.end_x = int(self.start_x + math.cos(angle) * length)
        self.end_y = int(self.start_y + math.sin(angle) * length)

        while game_map.get_at((self.end_x, self.end_y)) != OFF_TRACK_COLOR and length < MAX_SENSOR_LENGTH:
            length += 1
            self.end_x = int(self.start_x + math.cos(angle) * length)
            self.end_y = int(self.start_y + math.sin(angle) * length)

        dist = Sensor.get_distance(self.end_x, self.end_y, self.start_x, self.start_y) / self.sensivity
        return dist
    
    def draw(self, window):
        pygame.draw.line(window, SENSOR_COLOR, [self.start_x, self.start_y], [self.end_x, self.end_y], 1)
        pygame.draw.circle(window, SENSOR_COLOR, [self.end_x, self.end_y], 5)
