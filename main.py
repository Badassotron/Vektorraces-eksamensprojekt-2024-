import pygame
import math

# Initialize Pygame
pygame.init()



size = 600
grids = 40



# Set up the display window
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Pygame Window")

steps = int(size / grids)

white = 220, 210, 200
grey = 200, 190, 180
black = 40, 30, 20



# Window setup
def gridWindow():
    # Fill the window with white color
    window.fill((220, 210, 200))
    # And grid lines
    for x in range(1, grids):
        pygame.draw.line(window, grey, (0, (size / grids) * x), (size, (size / grids) * x), 2)

    for x in range(1, grids):
        pygame.draw.line(window, grey, ((size / grids) * x, 0), ((size / grids) * x, size), 2)



def main():
    while True:



        # Update the display
        pygame.display.flip()



if __name__ == "__main__":
    main()
