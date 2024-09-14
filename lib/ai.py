import neat
import pygame
from lib.car import Car
from lib.globals import *
from lib.controls import *

class AIController:
    def __init__(self, config_file, game_map, window):
        self.config = neat.config.Config(
            neat.DefaultGenome, 
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet, 
            neat.DefaultStagnation, 
            config_file
        )
        self.population = neat.Population(self.config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.population.add_reporter(neat.StatisticsReporter())
        self.game_map = game_map
        self.window = window

    def eval_genomes(self, genomes, config):
        cars = [Car(CAR_START_X, CAR_START_Y) for _ in genomes]
        nets = []
        ge = []

        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            genome.fitness = 0
            ge.append(genome)

        clock = pygame.time.Clock()
        start_time = pygame.time.get_ticks() 
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    quit()
                if pygame.key.get_pressed()[pygame.K_r]:
                    return

            self.window.fill((0, 0, 0))
            self.window.blit(self.game_map, (0, 0))

            all_cars_alive = any(car.alive for car in cars)
            if not all_cars_alive or pygame.time.get_ticks() - start_time > GENERATION_MAX_TIME * 1000:
                done = True

            for i, car in enumerate(cars):
                if car.alive:
                    inputs = car.get_ai_data()
                    output = nets[i].activate(inputs)

                    accelerate = output[0] > 0.5
                    brake = output[1] > 0.5
                    turn_left = output[2] > 0.5
                    turn_right = output[3] > 0.5

                    if accelerate:
                        car.accelerate()

                    if brake:
                        car.brake()

                    if turn_left:
                        car.turn_left()

                    if turn_right:
                        car.turn_right()

                    car.update(self.game_map)
                    car.draw(self.window)
                    if Sensor.draw_sensors:
                        car.draw_sensors(self.window)
                    ge[i].fitness += car.get_fitness()

            pygame.display.flip()
            clock.tick(60)

    def run(self):
        self.population.run(self.eval_genomes, 50)

