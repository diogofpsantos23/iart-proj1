import math
import time

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
        self.board = [1, 0, 0, 0, -1, 1, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, -1, 0, 1, 0, 0, 0,
                      0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, -1, 1, 0, 0, 0, -1]
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

    def print_menu(self):
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 128)

        title_text = title_font.render("ABOYNE", True, self.colors["BLACK"])
        title_rect = title_text.get_rect()
        title_rect.center = (self.screen.get_width() // 2, 250)

        text1 = font.render("1. Human vs Human", True, self.colors["DARKRED"])
        text2 = font.render("2. Human vs Computer", True, self.colors["DARKRED"])
        text3 = font.render("3. Computer vs Computer", True, self.colors["DARKRED"])

        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()

        text_rect1.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        text_rect2.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 40)
        text_rect3.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 80)

        self.screen.blit(text1, text_rect1)
        self.screen.blit(text2, text_rect2)
        self.screen.blit(text3, text_rect3)
        self.screen.blit(title_text, title_rect)

    def print_menu_difficulty(self):
        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 128)
        difficulty_font = pygame.font.Font(None, 64)

        title_text = title_font.render("ABOYNE", True, self.colors["BLACK"])
        title_rect = title_text.get_rect()
        title_rect.center = (self.screen.get_width() // 2, 210)

        difficulty_text = difficulty_font.render("Difficulty:", True, self.colors["DARKBLUE"])
        difficulty_rect = difficulty_text.get_rect()
        difficulty_rect.center = (self.screen.get_width() // 2, 320)

        text1 = font.render("1. Easy", True, self.colors["DARKRED"])
        text2 = font.render("2. Medium", True, self.colors["DARKRED"])
        text3 = font.render("3. Hard", True, self.colors["DARKRED"])

        text_rect1 = text1.get_rect()
        text_rect2 = text2.get_rect()
        text_rect3 = text3.get_rect()

        text_rect1.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 20)
        text_rect2.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 60)
        text_rect3.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 100)

        self.screen.blit(text1, text_rect1)
        self.screen.blit(text2, text_rect2)
        self.screen.blit(text3, text_rect3)
        self.screen.blit(title_text, title_rect)
        self.screen.blit(difficulty_text, difficulty_rect)

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

    def draw_goal_squares(self):
        square_size = 20  # Adjust the size as needed
        half_square_size = square_size // 2  # Calculate half size for positioning

        # Draw red square
        pygame.draw.rect(self.screen, self.colors["RED"],
                         (self.hexagon_centers[26][0] - half_square_size,
                          self.hexagon_centers[26][1] - half_square_size,
                          square_size,
                          square_size))

        # Draw blue square
        pygame.draw.rect(self.screen, self.colors["BLUE"],
                         (self.hexagon_centers[34][0] - half_square_size,
                          self.hexagon_centers[34][1] - half_square_size,
                          square_size,
                          square_size))

    def draw_board(self):
        for i in range(4, 0, -1):
            self.draw_line_of_hexagons(200 + i * 35, self.screen_height / 2 - i * 60, 9 - i)
        self.draw_line_of_hexagons(200, self.screen_height / 2, 9)
        for i in range(1, 5):
            self.draw_line_of_hexagons(200 + i * 35, self.screen_height / 2 + i * 60, 9 - i)
        self.draw_all_pieces()
        self.draw_goal_squares()

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

    def print_player_turn(self, current_player, erase=False):
        if erase: return
        font = pygame.font.Font(None, 48)
        blue_text = font.render("Blue's Turn", True, self.colors["BLUE"])
        red_text = font.render("Red's Turn", True, self.colors["RED"])
        if current_player == 1:
            self.screen.blit(blue_text, (20, 20))
        else:
            self.screen.blit(red_text, (self.screen.get_width() - red_text.get_width() - 20, 20))

    def print_player_wins(self, player):
        top_clear_rect = pygame.Rect(0, 0, self.screen_width, 60)
        pygame.draw.rect(self.screen, self.colors["WHITE"], top_clear_rect)
        font = pygame.font.Font(None, 48)
        blue_text = font.render("Blue Wins!", True, self.colors["BLUE"])
        red_text = font.render("Red Wins!", True, self.colors["RED"])
        if player == 1:
            self.screen.blit(blue_text, (20, 20))
        else:
            self.screen.blit(red_text, (self.screen.get_width() - red_text.get_width() - 20, 20))

    def print_draw(self):
        top_clear_rect = pygame.Rect(0, 0, self.screen_width, 60)
        pygame.draw.rect(self.screen, self.colors["WHITE"], top_clear_rect)
        font = pygame.font.Font(None, 48)
        text = font.render("Draw!", True, self.colors["BLACK"])
        text_width = text.get_width()
        x_coordinate = (self.screen_width - text_width) / 2
        self.screen.blit(text, (x_coordinate, 20))

    def display_results(self, blue_wins, red_wins, draws, n, difficulty):
        d = {2: 'Easy', 3: 'Medium', 4: 'Hard'}

        self.screen.fill((255, 255, 255))

        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 40)

        title_text = title_font.render(f"Statistics for {n} games", True, self.colors["BLACK"])
        title_text2 = title_font.render(f"Normal Blue CPU (depth 2) vs {d[difficulty]} Red CPU (depth {difficulty}):", True, self.colors["BLACK"])
        blue_text = font.render(f"Blue victories: {blue_wins}", True, self.colors["BLUE"])
        red_text = font.render(f"Red victories: {red_wins}", True, self.colors["RED"])
        draws_text = font.render(f"Draws: {draws}", True, self.colors["BLACK"])

        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 120))
        title_rect2 = title_text2.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 80))
        blue_rect = blue_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 20))
        red_rect = red_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 20))
        draws_rect = draws_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 60))

        self.screen.blit(blue_text, blue_rect)
        self.screen.blit(red_text, red_rect)
        self.screen.blit(draws_text, draws_rect)
        self.screen.blit(title_text, title_rect)
        self.screen.blit(title_text2, title_rect2)

        pygame.display.flip()
