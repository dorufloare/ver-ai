import pygame
from lib.globals import *
from lib.car import Car

def main():
    pygame.init()
    pygame.mixer.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Car Steering")

    car_image = pygame.image.load(CAR_IMAGE_PATH).convert_alpha()
    car = Car(car_image, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    cars = pygame.sprite.Group()
    cars.add(car)

    clock = pygame.time.Clock()
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            car.accelerate()
        if keys[pygame.K_s]:
            car.brake()
        if keys[pygame.K_a]:
            car.left_turn()
        if keys[pygame.K_d]:
            car.right_turn()

        cars.update()

        window.fill((0, 0, 0))
        cars.draw(window)
        for corner in car.get_corners():
            pygame.draw.circle(window, (255, 255, 0), (int(corner[0]), int(corner[1])), 5)
        pygame.display.flip()

        clock.tick_busy_loop(60)

    pygame.quit()

if __name__ == "__main__":
    main()
