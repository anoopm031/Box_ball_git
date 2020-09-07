import pygame
from math import hypot as hyp

pygame.init()

screen = pygame.display.set_mode((600,500))

colour = (0, 255, 0)

while 1:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            SystemExit

    center = (300, 250)
    radius = 100

    mpos = (0, 0)
    pygame.draw.circle(screen, colour, center, radius, 2)
    pygame.draw.circle(screen, colour, center, 2, 2)

    mpos = pygame.mouse.get_pos()
    # the important line which calculates the distance
    dist = hyp(center[0] - mpos[0], center[1] - mpos[1])
    #print(dist)
    # if distance is within the radius circle will be green, else red
    if dist > radius:

        colour = (255, 0, 0)
    else:
        colour = (0, 255, 0)

    pygame.display.update()