import pygame

class Track:
    def __init__(self, root, center):
        self.root = root
        self.image = pygame.image.load("Data/Graphics/map_3.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (1400, 800))
        self.rect = self.image.get_rect(center = center)
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        self.root.blit(self.image, self.rect)