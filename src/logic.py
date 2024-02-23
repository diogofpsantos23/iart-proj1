import sys
import pygame


class GameLogic:
    def __init__(self, game_draw):
        self.game_draw = game_draw
        self.board_indexes = [
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9, 10],
            [11, 12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23, 24, 25],
            [26, 27, 28, 29, 30, 31, 32, 33, 34],
            [35, 36, 37, 38, 39, 40, 41, 42],
            [43, 44, 45, 46, 47, 48, 49],
            [50, 51, 52, 53, 54, 55],
            [56, 57, 58, 59, 60]
        ]
        self.selected_piece_index = None
        self.highlighted_hexagons = []

    def check_hovered_piece(self):
        mouse_pos = pygame.mouse.get_pos()
        for i, center in enumerate(self.game_draw.hexagon_centers):
            x, y = center
            distance = (((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5)
            if distance < self.game_draw.hex_size:
                return i
        return None

    def highlight_possible_moves(self, piece_index):
        self.highlighted_hexagons = []
        left_border_indexes = [0, 5, 11, 18, 26, 35, 43, 50, 56]
        right_border_indexes = [4, 10, 17, 25, 34, 42, 49, 55, 60]
        piece_row = 0
        for row in self.board_indexes:
            if piece_index in row:
                break
            else:
                piece_row += 1

        # Horizontal Moves
        if piece_index in left_border_indexes:
            if self.game_draw.board[piece_index + 1] == 0:
                self.highlighted_hexagons.append(piece_index + 1)
        elif piece_index in right_border_indexes:
            if self.game_draw.board[piece_index - 1] == 0:
                self.highlighted_hexagons.append(piece_index - 1)
        else:
            if self.game_draw.board[piece_index + 1] == 0:
                self.highlighted_hexagons.append(piece_index + 1)
            if self.game_draw.board[piece_index - 1] == 0:
                self.highlighted_hexagons.append(piece_index - 1)

        # Diagonal Moves
        if piece_row == 0:
            j = self.board_indexes[0].index(piece_index)
            for i in self.board_indexes[1][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
        elif 0 < piece_row < 4:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j - 1:j + 1]:
                print(i)
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
            for i in self.board_indexes[piece_row + 1][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
        elif piece_row == 4:
            j = self.board_indexes[4].index(piece_index)
            for i in self.board_indexes[3][j - 1:j + 1]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
            for i in self.board_indexes[5][j - 1:j + 1]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
        elif 4 < piece_row < 8:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
            for i in self.board_indexes[piece_row + 1][j - 1:j + 1]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
        else:
            j = self.board_indexes[8].index(piece_index)
            for i in self.board_indexes[7][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)

    def move_piece(self, new_hexagon_index):
        self.game_draw.board[new_hexagon_index] = self.game_draw.board[self.selected_piece_index]
        self.game_draw.board[self.selected_piece_index] = 0
        self.selected_piece_index = None
        self.highlighted_hexagons = []

    def place_piece(self, hexagon_index, color):
        if self.game_draw.board[hexagon_index] != 0:
            return
        self.game_draw.board[hexagon_index] = 1 if color == self.game_draw.colors["BLUE"] else -1

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    clicked_piece_index = self.check_hovered_piece()
                    if clicked_piece_index is not None:
                        if self.selected_piece_index is None and self.game_draw.board[clicked_piece_index] != 0:
                            self.selected_piece_index = clicked_piece_index
                            self.highlight_possible_moves(clicked_piece_index)
                        else:
                            if clicked_piece_index in self.highlighted_hexagons:
                                self.move_piece(clicked_piece_index)
                            else:
                                self.selected_piece_index = None
                                self.highlighted_hexagons = []
                    else:
                        self.selected_piece_index = None
                        self.highlighted_hexagons = []
            self.game_draw.screen.fill(self.game_draw.colors["WHITE"])
            self.game_draw.draw_board()
            if self.selected_piece_index is not None:
                x, y = self.game_draw.hexagon_centers[self.selected_piece_index]
                if self.game_draw.board[self.selected_piece_index] == 1:
                    pygame.draw.circle(self.game_draw.screen, self.game_draw.colors["DARKBLUE"], (x, y), 20)
                elif self.game_draw.board[self.selected_piece_index] == -1:
                    pygame.draw.circle(self.game_draw.screen, self.game_draw.colors["DARKRED"], (x, y), 20)
            for hexagon_index in self.highlighted_hexagons:
                x, y = self.game_draw.hexagon_centers[hexagon_index]
                pygame.draw.circle(self.game_draw.screen, (0, 255, 0), (x, y), 10, width=10)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
