import pygame
import math
from lib.globals import *
from lib.sensor import Sensor
from lib.turntracker import TurnTracker

class Car(pygame.sprite.Sprite):
    rot_img = None
    base_image = None

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        if Car.base_image is None:
            Car.load_image()
            Car.precompute_rotations()

        self.image = Car.base_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.reversing = False
        self.heading = 0;
        self.speed = 0
        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(x, y)
        self.alive = True
        self.turn(0)
        self.turnTracker = TurnTracker()
        self.distance_driven = 0
        self.frames_alive = 0
         
        self.sensors = [
            Sensor(self.rect.centerx, self.rect.centery, -math.pi / 2),
            Sensor(self.rect.centerx, self.rect.centery, -math.pi / 4),
            Sensor(self.rect.centerx, self.rect.centery, 0),
            Sensor(self.rect.centerx, self.rect.centery, +math.pi / 4),
            Sensor(self.rect.centerx, self.rect.centery, +math.pi / 2)
        ]
        self.sensor_data = [0, 0, 0, 0, 0]

    @classmethod
    def load_image(cls):
        Car.base_image = pygame.image.load(CAR_IMAGE_PATH).convert_alpha()
        Car.base_image = pygame.transform.scale(Car.base_image, (CAR_WIDTH, CAR_HEIGHT))

    @classmethod
    def precompute_rotations(cls):
        cls.rot_img = [pygame.transform.rotozoom(Car.base_image, 360 - 90 - i, 1) for i in range(360)]

    @classmethod
    def get_quadrant(cls, angle):
        angle = angle % (2 * math.pi)
        if 0 <= angle < math.pi / 2:
            return 1
        elif math.pi / 2 <= angle < math.pi:
            return 2
        elif math.pi <= angle < 3 * math.pi / 2:
            return 3
        else:
            return 4

    @property
    def alive(self):
        return self._alive and (not self.is_very_slow())

    @alive.setter
    def alive(self, value):
        if isinstance(value, bool):
            self._alive = value
            if not value:
                self.speed = 0
                self.velocity = pygame.math.Vector2(0, 0)
        else:
            raise ValueError("Alive must be a boolean value")

    def turn(self, angle_degrees):
        self.heading += math.radians(angle_degrees)
        image_index = int(self.heading / math.radians(1)) % len(self.rot_img)
        if self.image != self.rot_img[image_index]:
            x, y = self.rect.center
            self.image = self.rot_img[image_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    def apply_overturn(self):
        turn_angle = self.turnTracker.get_angle()
        if turn_angle and self.speed > OVERSTEER_SPEED and turn_angle >= OVERSTEER_ANGLE:
            overturn_factor = (self.speed - OVERSTEER_SPEED) * OVERSTEER_INTENSITY
            self.heading += turn_angle * overturn_factor
        elif self.speed <= OVERSTEER_SPEED:
            self.heading = self.heading  # Keep the heading steady if under oversteer speed


    def turn_left(self, amount=TURN_SPEED):
        if self.speed < 0.1:
            return
        self.turn(-amount)

    def turn_right(self, amount=TURN_SPEED):
        if self.speed < 0.1:
            return
        self.turn(amount)

    def accelerate(self, amount=ACCELERATION_AMOUNT):
        if self.speed >= TOP_SPEED:
            return
        if not self.reversing:
            self.speed += amount
        else:
            self.speed -= amount

    def brake(self, amount=BRAKE_AMOUNT):
        if self.speed > 0:
            self.speed -= amount
            if self.speed < 0:
                self.speed = 0
        elif self.speed < 0:
            self.speed += amount
            if self.speed > 0:
                self.speed = 0

    def reverse(self):
        self.speed = 0
        self.reversing = not self.reversing

    def check_boundaries(self):
        if self.rect.left < 0:
            self.position.x = self.rect.width / 2
        if self.rect.right > WINDOW_WIDTH:
            self.position.x = WINDOW_WIDTH - self.rect.width / 2
        if self.rect.top < 0:
            self.position.y = self.rect.height / 2
        if self.rect.bottom > WINDOW_HEIGHT:
            self.position.y = WINDOW_HEIGHT - self.rect.height / 2

    def check_track_limits(self, game_map):
        car_corners = self.get_corners()
        for [x, y] in car_corners:
            if game_map.get_at((int(x), int(y))) == OFF_TRACK_COLOR:
                self.alive = False

    def update_sensors(self, game_map):
        sensor_data = []
        for sensor in self.sensors:
            sensor.start_x = self.rect.centerx
            sensor.start_y = self.rect.centery
            data = sensor.get_data(game_map, self.heading)
            sensor_data.append(data)

        return sensor_data
    
    def update(self, game_map):
        if not self.alive:
            self.speed = 0
            self.velocity = 0
            return
        self.apply_overturn()
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))
        self.position += self.velocity
        self.rect.center = (round(self.position[0]), round(self.position[1]))
        self.check_boundaries()
        if not IGNORE_TRACK_LIMITS:
            self.check_track_limits(game_map)
        self.sensor_data = self.update_sensors(game_map)
        self.turnTracker.track(self.heading)
        self.distance_driven += self.speed
        self.frames_alive += 1

    def draw_sensors(self, window):
        for sensor in self.sensors:
            sensor.draw(window)

    def get_corners(self):
        w, h = self.rect.size
        corners = [
            [self.rect.right, self.rect.top],
            [self.rect.right, self.rect.bottom],
            [self.rect.left, self.rect.top],
            [self.rect.left, self.rect.bottom],
        ]
        
        alpha = self.heading
        quadrant = Car.get_quadrant(alpha)
        x_offset = CAR_WIDTH * math.sin(alpha)
        y_offset = CAR_HEIGHT * math.sin(alpha)

        if quadrant == 1:
            corners[0][1] += y_offset
            corners[1][0] -= x_offset
            corners[2][0] += x_offset
            corners[3][1] -= y_offset
        if quadrant == 2:
            corners[0][0] -= x_offset
            corners[1][1] -= y_offset
            corners[2][1] += y_offset
            corners[3][0] += x_offset
        if quadrant == 3:
            corners[0][1] -= y_offset
            corners[1][0] += x_offset
            corners[2][0] -= x_offset
            corners[3][1] += y_offset
        if quadrant == 4:
            corners[0][0] += x_offset
            corners[1][1] += y_offset
            corners[2][1] -= y_offset
            corners[3][0] -= x_offset

        return corners
    
    def get_ai_data(self):
        ai_data = list(self.sensor_data) 
        ai_data.append(self.speed)
        ai_data.append(self.turnTracker.get_angle())        
        print(ai_data)
        return ai_data

    def get_fitness(self):
        if self.is_very_slow():
            return -10000
        return self.distance_driven
    
    def is_very_slow(self):
        return self.speed < LOWER_SPEED_LIMIT and self.frames_alive > 60

    def draw(self, window):
        window.blit(self.image, self.rect.topleft)