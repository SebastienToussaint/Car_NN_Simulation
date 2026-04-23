import math
import pygame
from sensors import DistanceSensor
from utilities import SaveDataStructure


class Car:
    def __init__(self, root, obstacles):
        # Movement vars
        self.position = [500, 500]

        # 270 = Straight up, 90 = straight down
        self.direction = 270
        # How fast forwards and right the car must move respectively
        self.move_vector = [0.0, 0.0]  # forward, right

        self.max_velocity = 5
        self.turn_rate = 3

        # Pygame visual vars
        self.image = pygame.image.load("Data/Graphics/car.png").convert_alpha()
        self.display_image = self.image
        self.rect = self.image.get_rect(center=self.position.copy())

        self.root = root


        self.sensors = [DistanceSensor(obstacles, 400, self.position, -45, self.root),
                        DistanceSensor(obstacles, 400, self.position, -30, self.root),
                        DistanceSensor(obstacles, 400, self.position, -15, self.root),
                        DistanceSensor(obstacles, 400, self.position, 0, self.root),
                        DistanceSensor(obstacles, 400, self.position, 15, self.root),
                        DistanceSensor(obstacles, 400, self.position, 30, self.root),
                        DistanceSensor(obstacles, 400, self.position, 45, self.root)
                        ]

        self.distances = []
        self.key_presses = []
        
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

    # Updates the direction that the car is moving
    # in degrees based on which keys the user is pressing
    def update_direction(self):
        directions = self.get_directions()

        if directions["forward"]:
            self.direction += ( self.turn_rate * directions["right"] - self.turn_rate * directions["left"])
        elif directions["backward"]:
            self.direction -= (self.turn_rate * directions["right"] - self.turn_rate * directions["left"])

        if self.direction >= 360:
            self.direction = 0
        elif self.direction < 0:
            self.direction = 360 + self.direction

    # Updates the movement vector of the car
    # to reflect the current traveling direction
    def update_move_vector(self):
        upwards_velocity = math.cos(math.radians(self.direction)) * self.max_velocity
        self.move_vector[1] = upwards_velocity

        right_velocity = math.sin(math.radians(self.direction)) * self.max_velocity
        self.move_vector[0] = right_velocity

    # Move the car, updating its position
    # with its movement vector
    def move(self):
        directions = self.get_directions()
        if directions["forward"]:
            # Update position
            self.position[0] += self.move_vector[1]
            self.position[1] += self.move_vector[0]
        elif directions["backward"]:
            self.position[0] -= self.move_vector[1]
            self.position[1] -= self.move_vector[0]

    # Update the image of the car so it rotates
    # smoothly and the rectangle matches the position
    def update_image(self):
        self.display_image = pygame.transform.rotate(self.image, -self.direction - 90)
        self.rect = self.display_image.get_rect(center = self.position)

    def display(self):
        self.root.blit(self.display_image, self.rect)

    # Call all the update functions and functions
    # needed for simulations
    def run(self):
        self.update_direction()
        self.update_move_vector()
        self.move()
        self.update_image()

        distances = []
        directions = self.get_directions()
        for s in self.sensors:
            distances.append(s.draw(self.direction))

        if directions["record"]:
            self.save_file.distances.append(distances)
            self.save_file.key_presses.append(directions)

        self.display()

    def neural_run(self, model):
        self.update_direction()
        self.update_move_vector()
        self.move()
        self.update_image()

        distances = []

        for s in self.sensors:
            distances.append(s.draw(self.direction))

        print(model.get_answer(distances))


        self.display()