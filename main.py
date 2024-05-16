import pygame
import math
import random

from grid import Grid
from grid import Tile
from vector import Vec


# Initialize Pygame
pygame.init()


size: int = 600  # Should scale with grids and be an equal number.
grids: int = 40  # Minimum 20 and should be an equal number.
widthR: int = 3  # Road width multiplier. Minimum 2. Should scale with grids.
roadComp: int = 5  # Complexity of the road. Lower numbers mean more complex roads. Should scale with road width.


# Make grid with classes
matrix = Grid(Vec(grids, grids))

# Set up the display window
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Pygame Window")

white = 220, 210, 200
grey = 130, 120, 110
red = 240, 80, 60
black = 40, 30, 20


roadMid = Vec(int(grids / 2), int(grids / 2))
roadR = int((roadMid.x + (roadMid.x - 10)) / 2)
startPos = Vec(0, 0)


def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


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

def vecm():
    mVec = Vec(startPos.x-1,startPos.y)
    for x in range(mVec.x - 2,mVec.x + 1):
        for y in range(mVec.y - 2, mVec.y + 1):
            matrix.get_tile_weight(Vec(x, y) + mVec)



# Road setup
def draw():
    for x in range(0, grids):
        for y in range(0, grids):
            if matrix.get_tile_weight(Vec(x, y)) >= 0:
                col = clamp(int(255 - matrix.get_tile_weight(Vec(x, y)) / 10), 0, 255), clamp(int(255 - matrix.get_tile_weight(Vec(x, y)) / 10), 0, 255), clamp(int(255 - matrix.get_tile_weight(Vec(x, y)) / 10), 0, 255)
                pygame.draw.rect(window, col, (x * (size / grids), y * (size / grids), (size / grids), (size / grids)))
            if matrix.get_tile_weight(Vec(x, y)) == -10:
                pygame.draw.rect(window, red, (x * (size / grids), y * (size / grids), (size / grids), (size / grids)))


def road():
    for angle in range(0, int(360 / roadComp)):
        roadVec = Vec(int(roadMid.x + roadR * math.cos(math.radians(angle * roadComp))), int(roadMid.y + roadR * math.sin(math.radians(angle * roadComp))))
        for x in range(roadVec.x - random.randint(1, widthR), roadVec.x + random.randint(1, widthR)):
            for y in range(roadVec.y - random.randint(1, widthR), roadVec.y + random.randint(1, widthR)):
                matrix.setTile(Vec(x, y), Tile(True, 0))


def flood():
    count = 0
    active = matrix.get_active_tiles()
    inactive = grids * grids - active
    weight = 0
    for steps in range(0, roadMid.y):
        if matrix.get_tile_weight(Vec(roadMid.x, steps)) >= 0:
            matrix.setTile(Vec(roadMid.x, steps), Tile(True, -10))

            count += 1
            if count == widthR - 1:
                startPos == Vec(roadMid.x - 1, steps)
                matrix.setTile(Vec(roadMid.x + 1, steps), Tile(True, 10))

    while active > 1:
        weight += 10
        active -= 1

        for x in range(grids):
            for y in range(grids):
                if matrix.get_tile_weight(Vec(x, y)) == weight:
                    for val in range(4):
                        if matrix.get_tile_weight(Vec(x, y + 1)) == 0:
                            matrix.setTile(Vec(x, y + 1), Tile(True, weight + 10))
                        if matrix.get_tile_weight(Vec(x, y - 1)) == 0:
                            matrix.setTile(Vec(x, y - 1), Tile(True, weight + 10))
                        if matrix.get_tile_weight(Vec(x + 1, y)) == 0:
                            matrix.setTile(Vec(x + 1, y), Tile(True, weight + 10))
                        if matrix.get_tile_weight(Vec(x - 1, y)) == 0:
                            matrix.setTile(Vec(x - 1, y), Tile(True, weight + 10))

    while inactive > 1:
        inactive -= 1

        for x in range(grids):
            for y in range(grids):
                if matrix.get_tile_weight(Vec(x, y)) == -2:
                    for val in range(4):
                        if matrix.get_tile_weight(Vec(x, y + 1)) == 0:
                            matrix.setTile(Vec(x, y + 1), Tile(True, matrix.get_tile_weight(Vec(x, y + 1)) + 5))
                        if matrix.get_tile_weight(Vec(x, y - 1)) == 0:
                            matrix.setTile(Vec(x, y - 1), Tile(True, matrix.get_tile_weight(Vec(x, y - 1)) + 5))
                        if matrix.get_tile_weight(Vec(x + 1, y)) == 0:
                            matrix.setTile(Vec(x + 1, y), Tile(True, matrix.get_tile_weight(Vec(x + 1, y)) + 5))
                        if matrix.get_tile_weight(Vec(x - 1, y)) == 0:
                            matrix.setTile(Vec(x - 1, y), Tile(True, matrix.get_tile_weight(Vec(x - 1, y)) + 5))


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
