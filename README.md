**Verstappen AI**
================

**Overview**
-----------

This project uses the NEAT (NeuroEvolution of Augmenting Topologies) algorithm to evolve artificial intelligence for a car racing game. The AI is trained to control a car on a game map, using a neural network to make decisions based on sensor data. The project also incorporates realistic physics, including oversteer, to create a more immersive and challenging game environment.

**Features**
------------

* **Evolutionary Algorithm**: The NEAT algorithm is used to evolve the AI over multiple generations, selecting for cars that perform well on the game map.
* **Neural Network Control**: The AI uses a neural network to make decisions based on sensor data, such as distance to obstacles and speed.
* **Game Map**: The game map is rendered using Pygame, and the car's position and sensors are updated in real-time.
* **Sensor Data**: The car's sensors provide data on its surroundings, which is used as input to the neural network.
* **Fitness Function**: The fitness function rewards cars that stay on the track, avoid obstacles, and maintain a high speed.
* **Realistic Physics**: The game incorporates realistic physics, including oversteer, to create a more immersive and challenging game environment.

**Usage**
---------

To run the project, simply execute the `main.py` file. This will start the NEAT algorithm, which will evolve the AI over multiple generations.

**Configuration**
---------------

The NEAT algorithm is configured using the `config_file` parameter, which specifies the settings for the evolution process. The `game_map` parameter specifies the game map to use, and the `window` parameter specifies the Pygame window to render the game in.

**Code Structure**
-----------------

The code is organized into several modules:

* `AIController`: This class manages the NEAT algorithm and the game loop.
* `Car`: This class represents the car, and provides methods for updating its position and sensors.
* `globals`: This module defines global constants, such as the car's starting position and the game map dimensions.

**Physics Implementation**
-------------------------

The game incorporates realistic physics, including oversteer, to create a more immersive and challenging game environment. The car's physics are updated in real-time, taking into account factors such as speed, oversteer, acceleration, and friction.

**License**
---------

This project is licensed under the MIT License. See `LICENSE` for details.

**Contributing**
--------------

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.
