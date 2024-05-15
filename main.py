import pygame
import math
import random

from grid import Grid
from grid import Tile
from vector import Vec


# Initialize Pygame
pygame.init()


size: int = 600  # Should scale with grids and be an equal number
grids: int = 30  # Minimum 20 and should be an equal number



# Make grid with classes
matrix = Grid(Vec(grids, grids))

# Set up the display window
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Pygame Window")

white = 220, 210, 200
grey = 200, 190, 180
red = 240, 80, 60
black = 40, 30, 20


roadMid = Vec(int(grids / 2), int(grids / 2))
roadR = int((roadMid.x + (roadMid.x - 10)) / 2)
startPos = Vec(0, 0)


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
                col = 255 - matrix.get_tile_weight(Vec(x, y)) * 2, 255 - matrix.get_tile_weight(Vec(x, y)) * 2, 255 - matrix.get_tile_weight(Vec(x, y)) * 2
                pygame.draw.rect(window, col, (x * (size / grids), y * (size / grids), (size / grids), (size / grids)))
            if matrix.get_tile_weight(Vec(x, y)) == -10:
                pygame.draw.rect(window, red, (x * (size / grids), y * (size / grids), (size / grids), (size / grids)))


def road():
    for angle in range(0, 180):
        roadVec = Vec(int(roadMid.x + roadR * math.cos(math.radians(angle * 2))), int(roadMid.y + roadR * math.sin(math.radians(angle * 2))))
        for x in range(roadVec.x - random.randint(1, 3), roadVec.x + random.randint(1, 3)):
            for y in range(roadVec.y - random.randint(1, 3), roadVec.y + random.randint(1, 3)):
                matrix.setTile(Vec(x, y), Tile(True, 0))


def flood():
    count = 0
    active = matrix.get_active_tiles()
    weight = 0
    for steps in range(0, roadMid.y):
        if matrix.get_tile_weight(Vec(roadMid.x, steps)) >= 0:
            matrix.setTile(Vec(roadMid.x, steps), Tile(True, -10))

            count += 1
            if count == 3:
                # startPos == Vec(roadMid.x - 1, steps)
                matrix.setTile(Vec(roadMid.x + 1, steps), Tile(True, 1))

    print("Active flood")

    while active > 1:
        weight += 1
        active -= 1

        for x in range(grids):
            for y in range(grids):
                if matrix.get_tile_weight(Vec(x, y)) == weight:
                    for val in range(4):
                        if matrix.get_tile_weight(Vec(x, y + 1)) == 0:
                            matrix.setTile(Vec(x, y + 1), Tile(True, weight + 1))
                        if matrix.get_tile_weight(Vec(x, y - 1)) == 0:
                            matrix.setTile(Vec(x, y - 1), Tile(True, weight + 1))
                        if matrix.get_tile_weight(Vec(x + 1, y)) == 0:
                            matrix.setTile(Vec(x + 1, y), Tile(True, weight + 1))
                        if matrix.get_tile_weight(Vec(x - 1, y)) == 0:
                            matrix.setTile(Vec(x - 1, y), Tile(True, weight + 1))


# Main loop
def main():
    first = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if first:
            road()
            flood()

            first = False

        gridWindow()


        # Update the display
        pygame.display.flip()



if __name__ == "__main__":
    main()
