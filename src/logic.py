import time

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
        self.adjacent_friendly_pieces = []
        self.adjacent_enemy_pieces = []

    def check_hovered_piece(self):
        mouse_pos = pygame.mouse.get_pos()
        for i, center in enumerate(self.game_draw.hexagon_centers):
            x, y = center
            distance = (((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5)
            if distance < self.game_draw.hex_size:
                return i
        return None

    def highlight_possible_moves(self, piece_index, current_player):
        self.highlighted_hexagons = []
        self.adjacent_friendly_pieces = []
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
            elif self.game_draw.board[piece_index + 1] == current_player:
                self.adjacent_friendly_pieces.append(piece_index + 1)
        elif piece_index in right_border_indexes:
            if self.game_draw.board[piece_index - 1] == 0:
                self.highlighted_hexagons.append(piece_index - 1)
            elif self.game_draw.board[piece_index - 1] == current_player:
                self.adjacent_friendly_pieces.append(piece_index - 1)
        else:
            if self.game_draw.board[piece_index + 1] == 0:
                self.highlighted_hexagons.append(piece_index + 1)
            if self.game_draw.board[piece_index - 1] == 0:
                self.highlighted_hexagons.append(piece_index - 1)
            if self.game_draw.board[piece_index + 1] == current_player:
                self.adjacent_friendly_pieces.append(piece_index + 1)
            if self.game_draw.board[piece_index - 1] == current_player:
                self.adjacent_friendly_pieces.append(piece_index - 1)

        # Diagonal Moves
        if piece_row == 0:
            j = self.board_indexes[0].index(piece_index)
            for i in self.board_indexes[1][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)
        elif 0 < piece_row < 4:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j - 1:j + 1]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)
            for i in self.board_indexes[piece_row + 1][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)
        elif piece_row == 4:
            j = self.board_indexes[4].index(piece_index)
            for i in self.board_indexes[3][j - 1:j + 1]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)
            for i in self.board_indexes[5][j - 1:j + 1]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)
        elif 4 < piece_row < 8:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)
            for i in self.board_indexes[piece_row + 1][j - 1:j + 1]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)
        else:
            j = self.board_indexes[8].index(piece_index)
            for i in self.board_indexes[7][j:j + 2]:
                if self.game_draw.board[i] == 0:
                    self.highlighted_hexagons.append(i)
                elif self.game_draw.board[i] == current_player:
                    self.adjacent_friendly_pieces.append(i)

        if current_player == 1 and 26 in self.highlighted_hexagons:
            self.highlighted_hexagons.remove(26)
        if current_player == -1 and 34 in self.highlighted_hexagons:
            self.highlighted_hexagons.remove(34)

        for i in self.adjacent_friendly_pieces:
            self.highlighted_hexagons += self.check_possible_captures(i, current_player)

        return self.highlighted_hexagons

    def check_possible_captures(self, piece_index, current_player):
        self.adjacent_enemy_pieces = []
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
            if self.game_draw.board[piece_index + 1] == -current_player:
                self.adjacent_enemy_pieces.append(piece_index + 1)
        elif piece_index in right_border_indexes:
            if self.game_draw.board[piece_index - 1] == -current_player:
                self.adjacent_enemy_pieces.append(piece_index - 1)
        else:
            if self.game_draw.board[piece_index + 1] == -current_player:
                self.adjacent_enemy_pieces.append(piece_index + 1)
            if self.game_draw.board[piece_index - 1] == -current_player:
                self.adjacent_enemy_pieces.append(piece_index - 1)

        # Diagonal Moves
        if piece_row == 0:
            j = self.board_indexes[0].index(piece_index)
            for i in self.board_indexes[1][j:j + 2]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)
        elif 0 < piece_row < 4:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j - 1:j + 1]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)
            for i in self.board_indexes[piece_row + 1][j:j + 2]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)
        elif piece_row == 4:
            j = self.board_indexes[4].index(piece_index)
            for i in self.board_indexes[3][j - 1:j + 1]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)
            for i in self.board_indexes[5][j - 1:j + 1]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)
        elif 4 < piece_row < 8:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j:j + 2]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)
            for i in self.board_indexes[piece_row + 1][j - 1:j + 1]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)
        else:
            j = self.board_indexes[8].index(piece_index)
            for i in self.board_indexes[7][j:j + 2]:
                if self.game_draw.board[i] == -current_player:
                    self.adjacent_enemy_pieces.append(i)

        return self.adjacent_enemy_pieces

    def move_piece(self, current_index, new_hexagon_index):
        self.game_draw.board[new_hexagon_index] = self.game_draw.board[current_index]
        self.game_draw.board[current_index] = 0
        self.selected_piece_index = None
        self.highlighted_hexagons = []
        self.adjacent_friendly_pieces = []
        self.adjacent_enemy_pieces = []

    def undo_move_piece(self, current_index, new_hexagon_index):
        self.game_draw.board[current_index] = self.game_draw.board[new_hexagon_index]
        self.game_draw.board[new_hexagon_index] = 0
        self.selected_piece_index = None
        self.highlighted_hexagons = []
        self.adjacent_friendly_pieces = []
        self.adjacent_enemy_pieces = []

    def check_blocked_piece(self, piece_index):
        team = self.game_draw.board[piece_index]
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
            if self.game_draw.board[piece_index + 1] == -team:
                return True
        elif piece_index in right_border_indexes:
            if self.game_draw.board[piece_index - 1] == -team:
                return True
        else:
            if self.game_draw.board[piece_index + 1] == -team:
                return True
            if self.game_draw.board[piece_index - 1] == -team:
                return True

        # Diagonal Moves
        if piece_row == 0:
            j = self.board_indexes[0].index(piece_index)
            for i in self.board_indexes[1][j:j + 2]:
                if self.game_draw.board[i] == -team:
                    return True
        elif 0 < piece_row < 4:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j - 1:j + 1]:
                if self.game_draw.board[i] == -team:
                    return True
            for i in self.board_indexes[piece_row + 1][j:j + 2]:
                if self.game_draw.board[i] == -team:
                    return True
        elif piece_row == 4:
            j = self.board_indexes[4].index(piece_index)
            for i in self.board_indexes[3][j - 1:j + 1]:
                if self.game_draw.board[i] == -team:
                    return True
            for i in self.board_indexes[5][j - 1:j + 1]:
                if self.game_draw.board[i] == -team:
                    return True
        elif 4 < piece_row < 8:
            j = self.board_indexes[piece_row].index(piece_index)
            for i in self.board_indexes[piece_row - 1][j:j + 2]:
                if self.game_draw.board[i] == -team:
                    return True
            for i in self.board_indexes[piece_row + 1][j - 1:j + 1]:
                if self.game_draw.board[i] == -team:
                    return True
        else:
            j = self.board_indexes[8].index(piece_index)
            for i in self.board_indexes[7][j:j + 2]:
                if self.game_draw.board[i] == -team:
                    return True

        return False

    def count_blocked_pieces(self):
        blocked_blue_pieces = 0
        blocked_red_pieces = 0
        for i in range(61):
            if self.game_draw.board[i] == 1 and self.check_blocked_piece(i):
                blocked_blue_pieces += 1
            elif self.game_draw.board[i] == -1 and self.check_blocked_piece(i):
                blocked_red_pieces += 1
        return blocked_blue_pieces, blocked_red_pieces

    def place_piece(self, hexagon_index, color):
        if self.game_draw.board[hexagon_index] != 0:
            return
        self.game_draw.board[hexagon_index] = 1 if color == self.game_draw.colors["BLUE"] else -1

    def highlight(self):
        if self.selected_piece_index is not None:
            x, y = self.game_draw.hexagon_centers[self.selected_piece_index]
            if self.game_draw.board[self.selected_piece_index] == 1:
                pygame.draw.circle(self.game_draw.screen, self.game_draw.colors["DARKBLUE"], (x, y), 20)
            elif self.game_draw.board[self.selected_piece_index] == -1:
                pygame.draw.circle(self.game_draw.screen, self.game_draw.colors["DARKRED"], (x, y), 20)

        for hexagon_index in self.highlighted_hexagons:
            x, y = self.game_draw.hexagon_centers[hexagon_index]
            if self.game_draw.board[hexagon_index] == 0:
                pygame.draw.circle(self.game_draw.screen, (0, 255, 0), (x, y), 10, width=10)
            else:
                pygame.draw.circle(self.game_draw.screen, (255, 255, 0), (x, y), 10, width=10)

        for piece_index in range(61):
            if self.game_draw.board[piece_index] != 0 and self.check_blocked_piece(piece_index):
                x, y = self.game_draw.hexagon_centers[piece_index]
                pygame.draw.circle(self.game_draw.screen, self.game_draw.colors["BLACK"], (x, y), 10, width=3)

    def get_possible_moves(self, player):
        moves = []
        for i in range(61):
            if self.game_draw.board[i] == player and not self.check_blocked_piece(i):
                for j in self.highlight_possible_moves(i, player):
                    moves.append((i, j))
        return moves

    def evaluate_f1(self):
        maximizing_player_pieces = sum(1 for i in self.game_draw.board if i == -1)
        minimizing_player_pieces = sum(1 for i in self.game_draw.board if i == 1)
        return maximizing_player_pieces - minimizing_player_pieces

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0:
            if len(self.get_possible_moves(maximizing_player)) == 0: return 0, None
            max_tuple = max(self.get_possible_moves(maximizing_player), key=lambda x: x[0])
            return max_tuple[0], max_tuple

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for (piece_index, new_index) in self.get_possible_moves(maximizing_player):
                self.move_piece(piece_index, new_index)
                eval, _ = self.minimax(depth - 1, alpha, beta, -1)
                # print(f"move=({piece_index}, {new_index}), eval={eval}")
                # self.undo_move_piece(piece_index, new_index)
                if eval > max_eval:
                    max_eval = eval
                    best_move = piece_index, new_index
                alpha = max(alpha, eval)
                # print(f"Maximizing, Depth: {depth}, Move: {piece_index, new_index}, Eval: {eval}, Max Eval: {max_eval}, Alpha: {alpha}, Beta: {beta}")
                if alpha >= beta:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for (piece_index, new_index) in self.get_possible_moves(maximizing_player):
                self.move_piece(piece_index, new_index)
                eval, _ = self.minimax(depth - 1, alpha, beta, 1)
                self.undo_move_piece(piece_index, new_index)
                if eval < min_eval:
                    min_eval = eval
                    best_move = piece_index, new_index
                beta = min(beta, eval)
                # print(f"Minimizing, Depth: {depth}, Move: {piece_index, new_index}, Eval: {eval}, Min Eval: {min_eval}, Alpha: {alpha}, Beta: {beta}")
                if alpha >= beta:
                    break
            return min_eval, best_move
