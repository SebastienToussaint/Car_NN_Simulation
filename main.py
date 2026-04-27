import os.path
from car import Car
import pygame
import pickle
from track import Track


# Initialise pygame and setup defaults
pygame.init()
root = pygame.display.set_mode([1500, 900])
clock = pygame.time.Clock()
fps = 30

# Initialize objects
track = Track(root, [750, 450])
car = Car(root, [track])

# Setup model if it exists
model = None
if os.path.exists("saved_model.pkl"):
    with open("saved_model.pkl", "rb") as file:
        model = pickle.load(file)

# Single update loop
def run_cycle(automatic):
    track.draw()
    if automatic and model  :
        car.neural_run(model)
    else:
        car.data_run()

# Simulation loop
run_simulation = True
while run_simulation:

    auto = False

     # EVENT LOOP
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            car.save_file.write_to_file("saved_data.pkl")
            run_simulation = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                car.save_file.write_to_file("saved_data.pkl")
                run_simulation = False


    # User holds space to activate automatic driving mode
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        auto = True


    # Simulation steps
    root.fill([100,100,100])

    run_cycle(auto)

    pygame.display.update()
    clock.tick(fps)
