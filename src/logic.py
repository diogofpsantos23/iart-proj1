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
                    vertical_gap = abs(4 - left_border_indexes.index(left))
                    break
        else:
            goal_cell = 26
            for left, right in zip(left_border_indexes, right_border_indexes):
                if left <= piece_index <= right:
                    horizontal_gap = abs(piece_index - left)
                    vertical_gap = abs(4 - left_border_indexes.index(left))
                    break
        return horizontal_gap + vertical_gap

    # Heuristic 1: Gives different scores to a piece's position according to its proximity to the middle lanes
    def evaluate_f1(self, player):
        counter = 0
        for i in range(61):
            if self.game_draw.board[i] == player:
                if i in [0, 1, 2, 3, 4] or i in [56, 57, 58, 59, 60]:
                    counter += 1
                elif i in [5, 6, 7, 8, 9, 10] or i in [50, 51, 52, 53, 54, 55]:
                    counter += 2
                elif i in [11, 12, 13, 14, 15, 16, 17] or i in [43, 44, 45, 46, 47, 48, 49]:
                    counter += 3
                else:
                    counter += 5
        return counter

    # Heuristic 2: Gives different scores to a piece's position according to its proximity to the goal cell
    def evaluate_f2(self, player):
        counter = 0
        for i in range(61):
            if self.game_draw.board[i] == player:
                counter += self.piece_distance_to_goal(i, player)
        return self.evaluate_f1(player) - counter*50

    # Heuristic 3: Returns the difference between blue and red pieces, prioritizing capture moves
    def evaluate_f3(self, player):
        if player == 1:
            return self.evaluate_f2(player) + sum(self.game_draw.board)*250
        else:
            return self.evaluate_f2(player) - sum(self.game_draw.board)*250

    # Heuristic 4: Returns the difference between possible capture moves
    def evaluate_f4(self, player):
        ally_possible_captures = 0
        enemy_possible_captures = 0
        for i in range(61):
            if not self.check_blocked_piece(i):
                if self.game_draw.board[i] == player:
                    ally_possible_captures += len(list(filter(lambda x: self.game_draw.board[x] == -player, self.highlight_possible_moves(i, player))))
                elif self.game_draw.board[i] == -player:
                    enemy_possible_captures += len(list(filter(lambda x: self.game_draw.board[x] == player, self.highlight_possible_moves(i, -player))))
        return self.evaluate_f3(player) + (ally_possible_captures - enemy_possible_captures)*15

    # Heuristic 5: Returns the difference between the number of pieces still able to play
    def evaluate_f5(self, player):
        blocked_blue, blocked_red = self.count_blocked_pieces()
        total_blue, total_red = self.game_draw.board.count(1), self.game_draw.board.count(-1)
        available_blue, available_red = total_blue - blocked_blue, total_red - blocked_red
        if player == 1:
            return self.evaluate_f4(player) + (available_blue - available_red)*20
        else:
            return self.evaluate_f4(player) + (available_red - available_blue)*20


    # Heuristic 6: If a move to the goal cell is possible, it's executed
    def evaluate_f6(self, player):
        if player == 1:
            if self.game_draw.board[34] == 1:
                return 1000000 + self.evaluate_f5(1)
        else:
            if self.game_draw.board[26] == -1:
                return 1000000 + self.evaluate_f5(-1)
        return self.evaluate_f5(player)

    # Heuristic 7: Block the other player's winning move
    def evaluate_f7(self, player):
        if player == 1:
            if self.game_draw.board[18] == -1 and not self.check_blocked_piece(18):
               if self.game_draw.board[27] == 1 or self.game_draw.board[35] == 1:
                   return 250 + self.evaluate_f6(1)
            if self.game_draw.board[27] == -1 and not self.check_blocked_piece(27):
                if self.game_draw.board[18] == 1 or self.game_draw.board[35] == 1:
                    return 250 + self.evaluate_f6(1)
            if self.game_draw.board[35] == -1 and not self.check_blocked_piece(35):
                if self.game_draw.board[18] == 1 or self.game_draw.board[27] == 1:
                    return 250 + self.evaluate_f6(1)
        else:
            if self.game_draw.board[25] == 1 and not self.check_blocked_piece(25):
                if self.game_draw.board[33] == -1 or self.game_draw.board[42] == -1:
                    return 250 + self.evaluate_f6(-1)
            if self.game_draw.board[33] == 1 and not self.check_blocked_piece(33):
                if self.game_draw.board[27] == -1 or self.game_draw.board[42] == -1:
                    return 250 + self.evaluate_f6(-1)
            if self.game_draw.board[42] == 1 and not self.check_blocked_piece(42):
                if self.game_draw.board[27] == -1 or self.game_draw.board[35] == -1:
                    return 250 + self.evaluate_f6(-1)
        return self.evaluate_f6(player)

    # Heuristic 8: If the other player has no available moves, just find the path to the goal cell
    def evaluate_f8(self, player):
        if len(self.get_possible_moves(-player)) == 0:
            return self.evaluate_f2(player)
        return self.evaluate_f7(player)

    def minimax(self, depth, alpha, beta, player, maximizing):
        if (depth == 0) or (len(self.get_possible_moves(player)) == 0 and maximizing) or (len(self.get_possible_moves(-player)) == 0 and not maximizing):
            return self.evaluate_f8(player), None

        if maximizing:
            available_moves = self.get_possible_moves(player)
            random.shuffle(available_moves)
            # print(f"\nAvailable moves for Player {player}: {available_moves}")
            max_eval = float('-inf')
            best_move = None
            for (piece_index, new_index) in available_moves:
                copy_board = tuple(self.game_draw.board)
                self.move_piece(piece_index, new_index)
                eval, _ = self.minimax(depth - 1, alpha, beta, player, False)
                self.game_draw.board = list(copy_board)
                if eval > max_eval:
                    max_eval = eval
                    best_move = piece_index, new_index
                alpha = max(alpha, eval)
                # print(f"Maximizing Player {player}, Depth: {depth}, Move: {piece_index, new_index}, Eval: {eval:.2f}, Max Eval: {max_eval:.2f}, Alpha: {alpha:.2f}, Beta: {beta:.2f}")
                if alpha >= beta:
                    break
            return max_eval, best_move
        else:
            available_moves = self.get_possible_moves(-player)
            random.shuffle(available_moves)
            # print(f"\nAvailable moves for Player {-player}: {available_moves}")
            min_eval = float('inf')
            best_move = None
            for (piece_index, new_index) in self.get_possible_moves(-player):
                copy_board = tuple(self.game_draw.board)
                self.move_piece(piece_index, new_index)
                eval, _ = self.minimax(depth - 1, alpha, beta, player, True)
                self.game_draw.board = list(copy_board)
                if eval < min_eval:
                    min_eval = eval
                    best_move = piece_index, new_index
                beta = min(beta, eval)
                # print(f"Minimizing Player {-player}, Depth: {depth}, Move: {piece_index, new_index}, Eval: {eval:.2f}, Min Eval: {min_eval:.2f}, Alpha: {alpha:.2f}, Beta: {beta:.2f}")
                if alpha >= beta:
                    break
            return min_eval, best_move
