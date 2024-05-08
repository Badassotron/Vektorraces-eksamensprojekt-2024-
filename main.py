import pygame

# Initialize Pygame
pygame.init()




size = 600
grids = 30



# Set up the display window
window = pygame.display.set_mode((size, size))
pygame.display.set_caption("Pygame Window")

steps = int(size / grids)

white = 220, 210, 200
grey = 200, 190, 180
black = 40, 30, 20



matrix2D = []



# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Fill the window with white color
    window.fill((220, 210, 200))
    # And grid lines
    for x in range(1, grids):
        pygame.draw.line(window, grey, (0, (size / grids) * x), (size, (size / grids) * x), 2)

    for x in range(1, grids):
        pygame.draw.line(window, grey, ((size / grids) * x, 0), ((size / grids) * x, size), 2)



    matrix2D = [[0] * steps] * steps

    print(matrix2D)



    # Update the display
    pygame.display.flip()