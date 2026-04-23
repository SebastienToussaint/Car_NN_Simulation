import pygame
import math

class DistanceSensor:
    def __init__(self, obstacles, max_distance, start_point, angle, root):
        self.max_distance = max_distance

        self.position = start_point
        self.angle = angle

        self.root = root
        self.obstacles = obstacles

        self.current_length = max_distance





    def get_distance(self, car_direction):
        absolute_angle = math.radians(-car_direction + 90 - self.angle)
        x_step = math.sin(absolute_angle)
        y_step = math.cos(absolute_angle)

        x ,y = 0, 0
        distance = 0
        while distance < self.max_distance:
            x += abs(x_step)
            y += abs(y_step)
            distance = math.sqrt(x ** 2 + y ** 2)
            for obstacle in self.obstacles:
                x_point = self.position[0] + x_step * distance
                y_point = self.position[1] + y_step * distance
                if obstacle.rect.collidepoint(x_point, y_point):

                    if obstacle.mask.get_at((x_point - obstacle.rect.x, y_point - obstacle.rect.y)):
                        return x_point, y_point, distance

        x_point = self.position[0] +  x_step * self.max_distance
        y_point = self.position[1] + y_step * self.max_distance

        return x_point, y_point, distance

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

    def draw(self, car_direction):
        x, y, distance = self.get_distance(car_direction)
        pygame.draw.line(self.root, "green", self.position, [x, y])
        pygame.draw.circle(self.root, "red", [x,y], 2)

        return distance

