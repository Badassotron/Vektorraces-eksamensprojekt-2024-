import pygame
import math
import random
import time

from grid import Grid
from grid import Tile
from vector import Vec


# Initialize Pygame
pygame.init()


# Main parameters for road generation and algorithm

size: int = 600  # Should scale with grids and be an equal number.
grids: int = 40  # Minimum 20 and should be an equal number.
widthR: int = 3  # Road width multiplier. Minimum 2. Should scale with grids.
roadComp: int = 5  # Complexity of the road. Lower numbers mean more complex roads. Should scale with road width.



# Grid generation
matrix = Grid(Vec(grids, grids))


# Set up the display window
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Pygame Window")
# Main colors for the display window
white = 220, 210, 200
grey = 130, 120, 110
red = 240, 80, 60
green = 80, 240, 60
black = 40, 30, 20


# Other variables
roadMid = Vec(int(grids / 2), int(grids / 2))
roadR = int((roadMid.x + (roadMid.x - 10)) / 2)
startPos = Vec(0, 0)

vectorSave = []
minVal: int = 0

finish: bool = False


# Clamp for math
def clamp(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


# Window setup
def draw():
    for x in range(0, grids):
        for y in range(0, grids):

            # Color the road
            if matrix.get_tile_weight(Vec(x, y)) >= 0:
                col = 255, clamp(int(255 - matrix.get_tile_weight(Vec(x, y)) / 14), 160, 255), clamp(int(255 - matrix.get_tile_weight(Vec(x, y)) / 7), 80, 255)
                pygame.draw.rect(window, col, (x * (size / grids), y * (size / grids), (size / grids), (size / grids)))

            # Color finish line
            if matrix.get_tile_weight(Vec(x, y)) == -10:
                pygame.draw.rect(window, red, (x * (size / grids), y * (size / grids), (size / grids), (size / grids)))

    # Color vectors
    for x in range(len(vectorSave)):
        vecx: Vec = vectorSave[x][0]
        vecy: Vec = vectorSave[x][1]
        pygame.draw.line(window, green, (vecx.x, vecx.y), (vecy.x, vecy.y), 2)


def gridWindow():
    window.fill(black)
    draw()

    # Add grid lines
    for x in range(1, grids):
        pygame.draw.line(window, grey, (0, (size / grids) * x), (size, (size / grids) * x), 2)

    for y in range(1, grids):
        pygame.draw.line(window, grey, ((size / grids) * y, 0), ((size / grids) * y, size), 2)


# Road generation and flooding
def road():
    # Activate random tiles in a circular shape
    for angle in range(0, int(360 / roadComp)):
        roadVec = Vec(int(roadMid.x + roadR * math.cos(math.radians(angle * roadComp))), int(roadMid.y + roadR * math.sin(math.radians(angle * roadComp))))
        for x in range(roadVec.x - random.randint(1, widthR), roadVec.x + random.randint(1, widthR)):
            for y in range(roadVec.y - random.randint(1, widthR), roadVec.y + random.randint(1, widthR)):
                matrix.setTile(Vec(x, y), Tile(True, 0))


def flood():
    count: int = 0
    active: int = matrix.get_active_tiles()
    inactive: int = grids * grids - active
    weight: int = 0

    # Generate finish line and first flood point
    for steps in range(0, roadMid.y):
        if matrix.get_tile_weight(Vec(roadMid.x, steps)) >= 0:
            matrix.setTile(Vec(roadMid.x, steps), Tile(True, -10))

            count += 1
            if count == widthR - 1:
                startPos = Vec(roadMid.x - 1, steps)
                print(startPos)
                matrix.setTile(Vec(roadMid.x + 1, steps), Tile(True, 10))

    # Main flooding of active tiles
    while active > 1:
        weight += 10
        active -= 1
        minVal = weight + 10

        for x in range(grids):
            for y in range(grids):
                if matrix.get_tile_weight(Vec(x, y)) == weight:
                    # Update values of the four tiles around the current tile
                    for val in range(4):
                        if matrix.get_tile_weight(Vec(x, y + 1)) == 0:
                            matrix.setTile(Vec(x, y + 1), Tile(True, weight + 10))
                        if matrix.get_tile_weight(Vec(x, y - 1)) == 0:
                            matrix.setTile(Vec(x, y - 1), Tile(True, weight + 10))
                        if matrix.get_tile_weight(Vec(x + 1, y)) == 0:
                            matrix.setTile(Vec(x + 1, y), Tile(True, weight + 10))
                        if matrix.get_tile_weight(Vec(x - 1, y)) == 0:
                            matrix.setTile(Vec(x - 1, y), Tile(True, weight + 10))

    # Overflooding of all tiles near a wall
    while inactive > 1:
        inactive -= 1

        for x in range(grids):
            for y in range(grids):
                if matrix.get_tile_weight(Vec(x, y)) == -2:
                    # Update values of the four tiles around the current tile
                    for val in range(4):
                        if matrix.get_tile_weight(Vec(x, y + 1)) == 0:
                            matrix.setTile(Vec(x, y + 1), Tile(True, matrix.get_tile_weight(Vec(x, y + 1)) + 5))
                        if matrix.get_tile_weight(Vec(x, y - 1)) == 0:
                            matrix.setTile(Vec(x, y - 1), Tile(True, matrix.get_tile_weight(Vec(x, y - 1)) + 5))
                        if matrix.get_tile_weight(Vec(x + 1, y)) == 0:
                            matrix.setTile(Vec(x + 1, y), Tile(True, matrix.get_tile_weight(Vec(x + 1, y)) + 5))
                        if matrix.get_tile_weight(Vec(x - 1, y)) == 0:
                            matrix.setTile(Vec(x - 1, y), Tile(True, matrix.get_tile_weight(Vec(x - 1, y)) + 5))


# Movement of vector algorithm
def vecMovement():
    moveVec: Vec = Vec(-1, 0)
    currentPos: Vec = startPos
    vectorCheck: Vec = Vec(0, 0)

    vecx: int = 0
    vecy: int = 0

    vecDone: bool = True

    while vecDone:
        for x in range(currentPos.x + moveVec.x - 2, currentPos.x + moveVec.x + 1):
            for y in range(currentPos.y + moveVec.y - 2, currentPos.y + moveVec.y + 1):
                if 0 < matrix.get_tile_weight(Vec(x, y)) < minVal:
                    vectorCheck = Vec(currentPos.x + moveVec.x + x, currentPos.y + moveVec.y + y)
                    minVal = matrix.get_tile_weight(Vec(x, y))

        print(minVal)

        for i in range(0, vectorCheck.x - 1):
            vecx += vectorCheck.x - i
        for j in range(0, vectorCheck.y - 1):
            vecy += vectorCheck.y - j

        if not matrix.get_tile_weight(Vec(vecx, vecy) + currentPos + vectorCheck) == -1 or -2:
            moveVec = vectorCheck
            vecDone = False
            vectorSave.append([Vec(currentPos.x, currentPos.y), Vec(moveVec.x, moveVec.y)])
            print(vecx)
            print(vecy)
            print(currentPos)
            print(vectorCheck)
            print(Vec(vecx, vecy) + currentPos + vectorCheck)
        else:
            matrix.setTile(vectorCheck, Tile(True, matrix.get_tile_weight(vectorCheck) + 50))
            print("Other")


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

        if finish == False:
            vecMovement()

        gridWindow()

        # Update the display
        pygame.display.flip()

        time.sleep(1)



if __name__ == "__main__":
    main()
