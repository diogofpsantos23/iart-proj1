import math

import pygame


class GameDraw:
    def __init__(self):
        pygame.init()
        self.screen_width = 960
        self.screen_height = 720
        self.hex_size = 40
        self.hex_width = self.hex_size * math.sqrt(3)
        self.hex_height = 2 * self.hex_size
        self.hexagon_centers = []
        self.board = [0] * 61
        self.colors = {
            "WHITE": (255, 255, 255),
            "BLACK": (0, 0, 0),
            "BEGE": (255, 255, 204),
            "RED": (255, 0, 0),
            "BLUE": (0, 0, 255),
            "DARKRED": (139, 0, 0),
            "DARKBLUE": (0, 0, 139)
        }
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Aboyne")

    def draw_hexagon(self, x, y):
        points = []
        center = (x, y)
        if len(self.hexagon_centers) < 61:
            self.hexagon_centers.append(center)
        for i in range(6):
            angle_deg = 30 + 60 * i
            angle_rad = math.radians(angle_deg)
            points.append((x + self.hex_size * math.cos(angle_rad),
                           y + self.hex_size * math.sin(angle_rad)))
        pygame.draw.polygon(self.screen, self.colors["BEGE"], points)
        pygame.draw.polygon(self.screen, self.colors["BLACK"], points, 3)

    def draw_line_of_hexagons(self, x, y, n):
        for i in range(n):
            x_ = x + i * self.hex_width
            y_ = y
            self.draw_hexagon(x_, y_)

    def draw_piece(self, x, y, color):
        pygame.draw.circle(self.screen, color, (x, y), 20)

    def draw_board(self):
        for i in range(4, 0, -1):
            self.draw_line_of_hexagons(200 + i * 35, self.screen_height / 2 - i * 60, 9 - i)
        self.draw_line_of_hexagons(200, self.screen_height / 2, 9)
        for i in range(1, 5):
            self.draw_line_of_hexagons(200 + i * 35, self.screen_height / 2 + i * 60, 9 - i)
        self.draw_all_pieces()

    def draw_all_pieces(self):
        for i in range(61):
            if self.board[i] == 1:
                self.draw_piece(self.hexagon_centers[i][0], self.hexagon_centers[i][1], self.colors["BLUE"])
            elif self.board[i] == -1:
                self.draw_piece(self.hexagon_centers[i][0], self.hexagon_centers[i][1], self.colors["RED"])
            elif self.board[i] == 2:
                self.draw_piece(self.hexagon_centers[i][0], self.hexagon_centers[i][1], self.colors["DARKBLUE"])
            elif self.board[i] == -2:
                self.draw_piece(self.hexagon_centers[i][0], self.hexagon_centers[i][1], self.colors["DARKRED"])
