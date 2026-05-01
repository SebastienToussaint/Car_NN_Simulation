import math
import os.path
import pickle

import pygame
from sympy.physics.quantum.gate import normalized

from sensors import DistanceSensor
from utilities import SaveDataStructure


class Car:
    """
    A simple model of a car, used for the purpose of data gathering for neural network training,
    as well as for the automatic neural network controlled driving of a car following training.
    The car has "distance sensors" mounted to it, that project forwards and detect objects and their
    distance to the car (imagine each sensor as a laser pointing in a specific direction).
    Multiple functions are included withing the class, including functions to fire all the lasers,
    display the car, move the car, and drive the car automatically via neural network control.
    """
    def __init__(self, root, obstacles):
        # Movement variables
        self.position = [500, 500]
        self.direction = 270  # 270 = Straight up, 90 = straight down
        self.move_vector = [0.0, 0.0]  # How fast forwards and right the car must move respectively

        # Constants
        self.MAX_VELOCITY = 5
        self.TURN_RATE = 4

        # Pygame visual variables
        self.image = pygame.transform.scale(pygame.image.load("Data/Graphics/car.png").convert_alpha(), [21, 40])
        self.display_image = self.image
        self.rect = self.image.get_rect(center=self.position.copy())
        self.root = root

        # Distance sensor initialization
        self.sensors = [DistanceSensor(obstacles, 400, self.position, -90, self.root),
                        DistanceSensor(obstacles, 400, self.position, -75, self.root),
                        DistanceSensor(obstacles, 400, self.position, -60, self.root),
                        DistanceSensor(obstacles, 400, self.position, -45, self.root),
                        DistanceSensor(obstacles, 400, self.position, -30, self.root),
                        DistanceSensor(obstacles, 400, self.position, -15, self.root),
                        DistanceSensor(obstacles, 400, self.position, 0, self.root),
                        DistanceSensor(obstacles, 400, self.position, 15, self.root),
                        DistanceSensor(obstacles, 400, self.position, 30, self.root),
                        DistanceSensor(obstacles, 400, self.position, 45, self.root),
                        DistanceSensor(obstacles, 400, self.position, 60, self.root),
                        DistanceSensor(obstacles, 400, self.position, 75, self.root),
                        DistanceSensor(obstacles, 400, self.position, 90, self.root)


                        ]

        # Data gathering variables
        self.distances = []
        self.key_presses = []

        if os.path.exists("Data/SaveFiles/saved_data.pkl"):
            print("Loading saved data file...")
            with open("Data/SaveFiles/saved_data.pkl", "rb") as file:
                self.save_file = pickle.load(file)
        else:
            print("Creating new data file...")
            self.save_file = SaveDataStructure()

    @staticmethod
    def get_directions():
        """
        Determines which direction keys the user is
        pressing.
        Returns a dictionary, containing boolean
        values for up, down, left and right respectively
        """
        keys = pygame.key.get_pressed()

        return {"forward" : keys[pygame.K_w],
                "backward" :keys[pygame.K_s],
                "left" :keys[pygame.K_a],
                "right" :keys[pygame.K_d],
                "record" :keys[pygame.K_l]}

    def update_direction(self, neural_net_directions = None):
        """
        Updates the direction that the car is moving
        in degrees based on which keys the user is pressing
        """
        if not neural_net_directions:
            directions = self.get_directions()
        else:
            directions = neural_net_directions

        if directions["forward"]:
            self.direction += ( self.TURN_RATE * directions["right"] - self.TURN_RATE * directions["left"])
        elif directions["backward"]:
            self.direction -= (self.TURN_RATE * directions["right"] - self.TURN_RATE * directions["left"])

        # Constrain the angle between 0 and 360 degrees
        if self.direction >= 360:
            self.direction = 0
        elif self.direction < 0:
            self.direction = 360 + self.direction

    def update_move_vector(self):
        """
        Updates the movement vector of the car
        to reflect the current traveling direction
        """
        upwards_velocity = math.cos(math.radians(self.direction)) * self.MAX_VELOCITY
        self.move_vector[1] = upwards_velocity

        right_velocity = math.sin(math.radians(self.direction)) * self.MAX_VELOCITY
        self.move_vector[0] = right_velocity

    def move(self, neural_net_directions = None):
        """
        Move the car, updating its position
        using its movement vector
        """
        if not neural_net_directions:
            directions = self.get_directions()
        else:
            directions = neural_net_directions

        if directions["forward"]:
            self.position[0] += self.move_vector[1]
            self.position[1] += self.move_vector[0]
        elif directions["backward"]:
            self.position[0] -= self.move_vector[1]
            self.position[1] -= self.move_vector[0]


    def update_image(self):
        """
        Rotate image of the car so it matches the angle of the car.
        Update the rectangle so it matches the rotated image
        """
        self.display_image = pygame.transform.rotate(self.image, -self.direction - 90)
        self.rect = self.display_image.get_rect(center = self.position)

    def display(self):
        """
        Display the car onto the root
        """
        self.root.blit(self.display_image, self.rect)


    def data_run(self, draw_lasers = True):
        """
        Call all the update functions and functions
        needed for data gathering runs.
        """
        self.update_direction()
        self.update_move_vector()
        self.move()
        self.update_image()

        distances = []
        directions = self.get_directions()
        for s in self.sensors:
            distances.append(s.simulate(self.direction, draw_lasers))

        if directions["record"] and directions["forward"]:
            print("Recording inputs")
            self.save_file.distances.append(distances)
            self.save_file.key_presses.append(directions)

        self.display()

    def neural_run(self, model, draw_lasers = True):
        """
        Call all the update functions and functions
        needed for neural network driving runs
        """
        # Get the distances from the sensors and calculate answer
        distances = []
        for s in self.sensors:
            distances.append(s.simulate(self.direction, draw_lasers))


        answer = model.get_answer(distances)
        print(answer)

        # Set inputs to match neural prediction
        inputs = {"forward": True,
                  "left": False,
                  "right": False,
                  "backward": False}

        if answer == "left":
            inputs["left"] = True
        elif answer == "right":
            inputs["right"] = True

        # Update car
        self.update_direction(inputs)
        self.update_move_vector()
        self.move(inputs)
        self.update_image()
        self.display()

