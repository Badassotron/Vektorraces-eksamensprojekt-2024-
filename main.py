import pygame
import math
import random

from grid import Grid
from grid import Tile
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

    draw()

    # And grid lines
    for x in range(1, grids):
        pygame.draw.line(window, grey, (0, (size / grids) * x), (size, (size / grids) * x), 2)

    for y in range(1, grids):
        pygame.draw.line(window, grey, ((size / grids) * y, 0), ((size / grids) * y, size), 2)


def square_validity_checker():
    while True:
        pass


# Road setup
def draw():
    for x in range(0, grids):
        for y in range(0, grids):
            if matrix.get_tile_weight(Vec(x, y)) >= 0:
                pygame.draw.rect(window, white, (x * (size / grids), y * (size / grids), (size / grids), (size / grids)))


def road():
    roadMid = Vec(int(grids / 2), int(grids / 2))
    roadR = int((roadMid.x + (roadMid.x - 10)) / 2)

    for angle in range(0, 180):
        roadVec = Vec(int(roadMid.x + roadR * math.cos(math.radians(angle * 2))), int(roadMid.y + roadR * math.sin(math.radians(angle * 2))))
        for x in range(roadVec.x - random.randint(1, 3), roadVec.x + random.randint(1, 3)):
            for y in range(roadVec.y - random.randint(1, 3), roadVec.y + random.randint(1, 3)):
                matrix.setTile(Vec(x, y), Tile(True, 0))


# Main loop
def main():
    road()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        gridWindow()


        # Update the display
        pygame.display.flip()



if __name__ == "__main__":
    main()
