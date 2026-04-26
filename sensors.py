import pygame
import math

class DistanceSensor:
    """
    A simple distance sensor that fires a laser in a certain direction
    and determines the distance to any object in that direction
    """
    def __init__(self, obstacles, max_distance, start_point, angle, root):
        self.max_distance = max_distance

        self.position = start_point
        self.angle = angle

        self.root = root
        self.obstacles = obstacles

        self.current_length = max_distance

    def get_distance(self, car_direction):
        """
        Checks for mesh collisions along the path of the laser.
        If a mesh collision (object) is detected before the max range
        of the laser, returns the distance to the object
        (otherwise just returns the max range).
        """
        absolute_angle = math.radians(-car_direction + 90 - self.angle)
        x_step = math.sin(absolute_angle)
        y_step = math.cos(absolute_angle)

        x ,y = 0, 0
        distance = 0

        # Check for mesh collision at each interval
        # in the direction of the laser
        while distance < self.max_distance:
            x += abs(x_step)
            y += abs(y_step)
            distance = math.sqrt(x ** 2 + y ** 2)
            # Iterate through each object
            for obstacle in self.obstacles:
                x_point = self.position[0] + x_step * distance
                y_point = self.position[1] + y_step * distance
                # If we're within the rectangle of the object, then check for mesh
                # collision. This is done because rectangle collision detection
                # is much less demanding than mech collision detection
                if obstacle.rect.collidepoint(x_point, y_point):
                    if obstacle.mask.get_at((x_point - obstacle.rect.x, y_point - obstacle.rect.y)):
                        # Collision found, return location of collision and distance from car
                        return x_point, y_point, distance

        x_point = self.position[0] +  x_step * self.max_distance
        y_point = self.position[1] + y_step * self.max_distance

        # No collision found, return coordinates of tip of laser and distance from car
        return x_point, y_point, distance


    # COULD BE A GOOD WAY TO OPTIMIZE LASER OBJECT DETECTION VIA A BINARY SEARCH PATTERN
    # def get_endpoints_binary_search(self, obstacle, endpoints, prev_point, x_step, y_step):
    #     obstacle_at_endpoint =
    #     obstacle_edge = obstacle.mask.get_at((endpoints[0] - x_step - obstacle.rect.x, endpoints[1] - y_step - obstacle.rect.y))
    #
    #     if obstacle_at_endpoint and not obstacle_edge:
    #         # Found the edge of the obstacle
    #         return endpoints
    #     elif not obstacle_at_endpoint:
    #         # Need to go further up
    #         pass
    #     else:
    #         # Need to go further down
    #         pass
    #
    #     return 1

    def simulate(self, car_direction):
        """
        Fires the laser, checks for object collision,
        draws the laser, and returns it calculated
        distance to object.
        """
        x, y, distance = self.get_distance(car_direction)
        pygame.draw.line(self.root, "green", self.position, [x, y])
        pygame.draw.circle(self.root, "red", [x,y], 2)

        return distance

