import pygame
import math
import random
import time

from grid import Grid
from grid import Tile
from vector import Vec
from vector import VecLine


# Initialize Pygame
pygame.init()


# Main parameters for road generation and algorithm

size: int = 600  # Should scale with grids and be an equal number.
grids: int = 40  # Minimum 20 and should be an equal number.
widthR: int = 3  # Road width multiplier. Minimum 2. Should scale with grids.
roadComp: int = 1  # Complexity of the road. Lower numbers mean more complex roads. Should scale with road width.



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
count: int = 0

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


def gridWindow():
    window.fill(black)
    draw()

    # Add grid lines
    for x in range(1, grids):
        pygame.draw.line(window, grey, (0, (size / grids) * x), (size, (size / grids) * x), 2)

    for y in range(1, grids):
        pygame.draw.line(window, grey, ((size / grids) * y, 0), ((size / grids) * y, size), 2)

    # Color vectors
    for i in range(len(vectorSave)):
        pygame.draw.line(window, green, (vectorSave[i].start.x * int(size / grids) + int((size / grids) / 2), vectorSave[i].start.y * int(size / grids) + int((size / grids) / 2)), (vectorSave[i].end.x * int(size / grids) + int((size / grids) / 2), vectorSave[i].end.y * int(size / grids) + int((size / grids) / 2)), 4)

    # Update the display
    pygame.display.flip()


# Road generation and flooding
def road():
    # Activate random tiles in a circular shape
    for angle in range(0, int(360 / roadComp)):
        roadVec = Vec(int(roadMid.x + roadR * math.cos(math.radians(angle * roadComp))), int(roadMid.y + roadR * math.sin(math.radians(angle * roadComp))))
        for x in range(roadVec.x - random.randint(1, widthR), roadVec.x + random.randint(1, widthR)):
            for y in range(roadVec.y - random.randint(1, widthR), roadVec.y + random.randint(1, widthR)):
                matrix.setTile(Vec(x, y), Tile(True, 0))


def flood():
    c: int = 0
    active: int = matrix.get_active_tiles()
    inactive: int = grids * grids - active
    weight: int = 0
    startVecTemp: Vec = Vec(0, 0)


    # Generate finish line and first flood point
    for steps in range(0, roadMid.y):
        if matrix.get_tile_weight(Vec(roadMid.x, steps)) >= 0:
            matrix.setTile(Vec(roadMid.x, steps), Tile(True, -10))

            c += 1
            if c == widthR - 1:
                startVecTemp = Vec(roadMid.x - 1, steps)
                matrix.setTile(Vec(roadMid.x + 1, steps), Tile(True, 10))

    # Main flooding of active tiles
    while active > 1:
        weight += 10
        active -= 1

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

    return startVecTemp


# Movement of vector algorithm
def vecMovement(t, save):
    moveVec: Vec = Vec(save[t].end.x - save[t].start.x, save[t].end.y - save[t].start.y)
    currentPos: Vec = save[t].end

    tempVec: Vec = Vec(0, 0)
    minVal: int = matrix.get_tile_weight(currentPos)

    vecx: int = 0
    vecy: int = 0

    vecDone: bool = True

    while vecDone:
        for x in range(currentPos.x + moveVec.x - 1, currentPos.x + moveVec.x + 2):
            for y in range(currentPos.y + moveVec.y - 1, currentPos.y + moveVec.y + 2):
                vectorCheck = Vec(x, y)
                if 0 < matrix.get_tile_weight(vectorCheck) <= minVal:
                    tempVec = vectorCheck
                    minVal = matrix.get_tile_weight(vectorCheck)

        moveVec = tempVec - currentPos
        moveVecPlus: Vec = Vec(int(abs(moveVec.x)), int(abs(moveVec.y)))

        for i in range(0, moveVecPlus.x - 1):
            vecx += moveVecPlus.x - i
        for j in range(0, moveVecPlus.y - 1):
            vecy += moveVecPlus.y - j

        if matrix.get_tile_weight(Vec(vecx, vecy) + tempVec) > 0:
            vecDone = False
            save.append(VecLine(currentPos, tempVec))
        else:
            if not matrix.get_tile_weight(tempVec) < 0:
                matrix.setTile(tempVec, Tile(True, matrix.get_tile_weight(tempVec) + 50))

            pygame.draw.line(window, red, (currentPos.x * int(size / grids) + int((size / grids) / 2), currentPos.y * int(size / grids) + int((size / grids) / 2)), (tempVec.x * int(size / grids) + int((size / grids) / 2), tempVec.y * int(size / grids) + int((size / grids) / 2)), 4)

            time.sleep(0.5)

            moveVec: Vec = Vec(save[t].end.x - save[t].start.x, save[t].end.y - save[t].start.y)
            currentPos: Vec = save[t].end

            tempVec: Vec = Vec(0, 0)
            minVal: int = matrix.get_tile_weight(currentPos)

            vecx: int = 0
            vecy: int = 0

            vecDone: bool = True


            # Update the display
            pygame.display.flip()


# Main loop
def main(t):
    first = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if first:
            road()
            startPosTemp = flood()
            vectorSave.append(VecLine(Vec(startPosTemp.x + 1, startPosTemp.y), startPosTemp))
            print(startPosTemp)

            first = False


        if not finish:
            vecMovement(t, vectorSave)
            t += 1

        gridWindow()

        time.sleep(0.5)



if __name__ == "__main__":
    main(count)
