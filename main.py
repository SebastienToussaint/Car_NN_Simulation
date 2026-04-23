from car import Car
import pygame
from track import Track

root = pygame.display.set_mode([1500, 900])
clock = pygame.time.Clock()

track = Track(root, [750, 450])
car = Car(root, [track])

min_fps = 150

def run_cycle():
    track.draw()
    car.run()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            car.save_file.write_to_file("saved_data2.pkl")
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                car.save_file.write_to_file("saved_data2.pkl")
                pygame.quit()

    root.fill([100,100,100])

    run_cycle()

    pygame.display.update()
    if clock.get_fps() < min_fps and clock.get_fps() != 0:
        min_fps = clock.get_fps()
        print(min_fps)
    clock.tick(30)