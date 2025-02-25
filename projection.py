import pygame
import numpy as np
import math
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0,0,0)

WIDTH, HEIGHT = 800, 600
pygame.display.set_caption("3D projection")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100
circle_pos = [WIDTH/2, HEIGHT/2]

angle = 0

points = []
points.append(np.matrix([-1,-1,1]))
points.append(np.matrix([1,-1,1]))
points.append(np.matrix([1,1,1]))
points.append(np.matrix([-1,1,1]))
points.append(np.matrix([-1,-1,-1]))
points.append(np.matrix([1,-1,-1]))
points.append(np.matrix([1,1,-1]))
points.append(np.matrix([-1,1,-1]))

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]])



projected_points = [[n,n] for n in range(len(points))]
def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    rotation_z = np.matrix([[np.cos(angle), -np.sin(angle), 0],
                            [np.sin(angle), np.cos(angle), 0],
                            [0, 0, 1]])
    rotation_y = np.matrix([[np.cos(angle),0, np.sin(angle)],
                            [0, 1, 0],
                            [-np.sin(angle), 0, np.cos(angle)]
                            ])
    rotation_x = np.matrix([[1,0,0],
                            [0, np.cos(angle), -np.sin(angle)],
                            [0, np.sin(angle), np.cos(angle)]])

    angle += 0.01
    screen.fill(WHITE)

    i = 0
    for point in points:
        rotate2D = np.dot(rotation_z, point.reshape(3,1))
        rotate2D = np.dot(rotation_y, rotate2D)
        rotate2D = np.dot(rotation_x, rotate2D)
        projected2d = np.dot(projection_matrix, rotate2D)


        x = int(projected2d[0][0]*scale) + circle_pos[0]
        y = int(projected2d[1][0]*scale) + circle_pos[1]

        projected_points[i] = [x,y]
        pygame.draw.circle(screen, BLACK, (x, y),5)
        i += 1


    for p in range(4):
        connect_points(p, (p+1)%4, projected_points)
        connect_points(p+4, (p+1)%4+4, projected_points)
        connect_points(p, p+4, projected_points)


    pygame.display.update()