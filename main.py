import pygame
# import math

from grid import Grid
from vector import Vec

# Initialize Pygame
pygame.init()



size: int = 600
grids: int = 40



# Make grid with classes
matrix = Grid(Vec(grids, grids))

# Set up the display window
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Pygame Window")

white = 220, 210, 200
grey = 200, 190, 180
black = 40, 30, 20





# Window setup
def gridWindow():
    # Fill the window with white color
    window.fill(black)

    road()

    # And grid lines
    for x in range(1, grids):
        pygame.draw.line(window, grey, (0, (size / grids) * x), (size, (size / grids) * x), 2)

    for y in range(1, grids):
        pygame.draw.line(window, grey, ((size / grids) * y, 0), ((size / grids) * y, size), 2)

def square_validity_checker():
    while True


# Road setup
def road():
    for x in range(0, grids):
        for y in range(0, grids):
            if matrix.get_tile_weight(Vec(x, y)) >= 0:
                pygame.draw.rect(window, white, (x, y, (size / grids), (size / grids)))


# Main loop
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        gridWindow()


        # Update the display
        pygame.display.flip()



if __name__ == "__main__":
    main()
