import pygame
import sys
import math

pygame.init()
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720
HEX_SIZE = 40
HEX_WIDTH = HEX_SIZE * math.sqrt(3)
HEX_HEIGHT = 2 * HEX_SIZE
HEXAGON_CENTERS = []
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEGE = (255, 255, 204)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Aboyne")


def draw_hexagon(x, y):
    points = []
    center = (x, y)
    if (len(HEXAGON_CENTERS) < 61): HEXAGON_CENTERS.append(center)
    for i in range(6):
        angle_deg = 30 + 60 * i
        angle_rad = math.radians(angle_deg)
        points.append((x + HEX_SIZE * math.cos(angle_rad),
                       y + HEX_SIZE * math.sin(angle_rad)))
    pygame.draw.polygon(screen, BEGE, points)
    pygame.draw.polygon(screen, BLACK, points, 3)


def draw_line_of_hexagons(x, y, n):
    for i in range(n):
        x_ = x + i * HEX_WIDTH
        y_ = y
        draw_hexagon(x_, y_)


def draw_ball(x, y, color):
    pygame.draw.circle(screen, color, (x, y), 20)


def draw_board():
    for i in range(4, 0, -1):
        draw_line_of_hexagons(200 + i * 35, SCREEN_HEIGHT / 2 - i * 60, 9 - i)
    draw_line_of_hexagons(200, SCREEN_HEIGHT / 2, 9)
    for i in range(1, 5):
        draw_line_of_hexagons(200 + i * 35, SCREEN_HEIGHT / 2 + i * 60, 9 - i)
    draw_ball(HEXAGON_CENTERS[0][0], HEXAGON_CENTERS[0][1], RED)
    draw_ball(HEXAGON_CENTERS[1][0], HEXAGON_CENTERS[1][1], BLUE)
    draw_ball(HEXAGON_CENTERS[7][0], HEXAGON_CENTERS[7][1], BLUE)


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(WHITE)
        draw_board()
        pygame.display.flip()
    for i in range(61):
        print(f"Hexagon {i}: ({round(HEXAGON_CENTERS[i][0], 2)}, {HEXAGON_CENTERS[i][1]})")
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
