import pygame
import random

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

    def reset_board(self):
        self.game_draw.board = [1, 0, 0, 0, -1, 1, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, 0, -1, 0, 1,
                                0, 0, 0, 0, 0, -1, 0, 1, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, -1,
                                1, 0, 0, 0, -1]

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
            if len(self.board_indexes[piece_row - 1][j - 1:j + 1]) == 0:
                for i in self.board_indexes[piece_row - 1][j:j + 1]:
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
            if len(self.board_indexes[piece_row + 1][j - 1:j + 1]) == 0:
                for i in self.board_indexes[piece_row + 1][j:j + 1]:
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
            if len(self.board_indexes[piece_row - 1][j - 1:j + 1]) == 0:
                for i in self.board_indexes[piece_row - 1][j:j + 1]:
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
            if len(self.board_indexes[piece_row + 1][j - 1:j + 1]) == 0:
                for i in self.board_indexes[piece_row + 1][j:j + 1]:
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
            if len(self.board_indexes[piece_row - 1][j - 1:j + 1]) == 0:
                for i in self.board_indexes[piece_row - 1][j:j + 1]:
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
            if len(self.board_indexes[piece_row + 1][j - 1:j + 1]) == 0:
                for i in self.board_indexes[piece_row + 1][j:j + 1]:
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

    def piece_distance_to_goal(self, piece_index, player):
        global horizontal_gap, vertical_gap, goal_cell
        left_border_indexes = [0, 5, 11, 18, 26, 35, 43, 50, 56]
        right_border_indexes = [4, 10, 17, 25, 34, 42, 49, 55, 60]
        if player == 1:
            goal_cell = 34
            for left, right in zip(left_border_indexes, right_border_indexes):
                if left <= piece_index <= right:
                    horizontal_gap = abs(piece_index - right)
                    vertical_gap = abs(4 - left_border_indexes.index(right))
                    break
        else:
            goal_cell = 26
            for left, right in zip(left_border_indexes, right_border_indexes):
                if left <= piece_index <= right:
                    horizontal_gap = abs(piece_index - left)
                    vertical_gap = abs(4 - left_border_indexes.index(left))
                    break
        return horizontal_gap + vertical_gap

    def piece_distance_to_mid_lane(self, piece_index):
        global horizontal_gap, vertical_gap, goal_cell
        left_border_indexes = [0, 5, 11, 18, 26, 35, 43, 50, 56]
        right_border_indexes = [4, 10, 17, 25, 34, 42, 49, 55, 60]
        goal_cell = 26
        for left, right in zip(left_border_indexes, right_border_indexes):
            if left <= piece_index <= right:
                vertical_gap = abs(4 - left_border_indexes.index(left))
                break
        return vertical_gap

    # Heuristic 1: Returns the difference between red and blue pieces, prioritizing capture moves
    def evaluate_f1(self, player):
        if player == 1:
            return sum(self.game_draw.board)
        else:
            return -sum(self.game_draw.board)

    # Heuristic 2: Factors in the total distance of all pieces to the goal cell, making them get closer to it
    def evaluate_f2(self, player):
        total_distance_to_goal = 0
        for i in range(61):
            if self.game_draw.board[i] == player:
                total_distance_to_goal += self.piece_distance_to_goal(i, player)
        return self.evaluate_f1(player) * 1000 + (1 / (total_distance_to_goal + 1)) * 1000

    # Heuristic 3: If a move to the goal cell is possible, it's executed
    def evaluate_f3(self, player):
        if player == 1:
            if self.game_draw.board[34] == 1:
                return 100000 + self.evaluate_f2(1)
        else:
            if self.game_draw.board[26] == -1:
                return 100000 + self.evaluate_f2(-1)
        return self.evaluate_f2(player)

    # Heuristic 4: Factors in the total distance of all pieces to the middle row of the board, making them get closer to it
    def evaluate_f4(self, player):
        total_distance_to_mid_lane = 0
        for i in range(61):
            if self.game_draw.board[i] == player:
                total_distance_to_mid_lane += self.piece_distance_to_mid_lane(i)
        return (1 / (total_distance_to_mid_lane + 1)) * 100 + self.evaluate_f3(player)

    # Heuristic 5: Factors in the total possible capture moves the enemy player has available
    def evaluate_f5(self, player):
        total_enemy_possible_captures = 0
        for i in range(61):
            if self.game_draw.board[i] == -player:
                total_enemy_possible_captures += len(self.check_possible_captures(i, -player))
        return self.evaluate_f4(player) / (total_enemy_possible_captures+1)

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0:
            if len(self.get_possible_moves(maximizing_player)) == 0:
                return 0, None
            return self.evaluate_f5(maximizing_player), None

        if maximizing_player:
            max_eval = float('-inf')
            best_moves = []
            for (piece_index, new_index) in self.get_possible_moves(maximizing_player):
                copy_board = tuple(self.game_draw.board)
                self.move_piece(piece_index, new_index)
                eval, _ = self.minimax(depth - 1, alpha, beta, -1)
                self.game_draw.board = list(copy_board)
                if eval > max_eval:
                    max_eval = eval
                    best_moves = [(piece_index, new_index)]
                elif eval == max_eval:
                    best_moves.append((piece_index, new_index))
                alpha = max(alpha, eval)
                if alpha >= beta:
                    break
            return max_eval, random.choice(best_moves) if best_moves else None
        else:
            min_eval = float('inf')
            best_move = None
            for (piece_index, new_index) in self.get_possible_moves(maximizing_player):
                copy_board = tuple(self.game_draw.board)
                self.move_piece(piece_index, new_index)
                eval, _ = self.minimax(depth - 1, alpha, beta, -1)
                self.game_draw.board = list(copy_board)
                if eval < min_eval:
                    min_eval = eval
                    best_move = piece_index, new_index
                beta = min(beta, eval)
                if alpha >= beta:
                    break
            return min_eval, best_move