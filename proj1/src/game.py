import random
import sys
import time
import pygame
from draw import GameDraw
from logic import GameLogic


class AboyneGame:
    def __init__(self):
        self.game_draw = GameDraw()
        self.game_logic = GameLogic(self.game_draw)
        self.current_player = random.choice([1, -1])

    # This function runs the inital menu of the application
    def menu(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.play_human_vs_human()
                    elif event.key == pygame.K_2:
                        self.menu_difficulty(1)
                    elif event.key == pygame.K_3:
                        self.menu_difficulty(2)

            self.game_draw.screen.fill(self.game_draw.colors["WHITE"])
            self.game_draw.print_menu()
            pygame.display.flip()

    # This function runs the difficulty menu after the user picked one of the following game modes: Human vs CPU or CPU vs CPU
    def menu_difficulty(self, mode):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.menu()

                if mode == 1:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.play_human_vs_computer(1)
                        elif event.key == pygame.K_2:
                            self.play_human_vs_computer(2)
                        elif event.key == pygame.K_3:
                            self.play_human_vs_computer(3)

                elif mode == 2:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.play_computer_vs_computer(3, 1)
                        elif event.key == pygame.K_2:
                            self.play_computer_vs_computer(2, 2)
                        elif event.key == pygame.K_3:
                            self.play_computer_vs_computer(1, 3)

            self.game_draw.screen.fill(self.game_draw.colors["WHITE"])
            self.game_draw.print_menu_difficulty()
            pygame.display.flip()

    # This function executes a single game of Human vs Human
    def play_human_vs_human(self):
        self.game_logic.reset_board()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.menu()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                    clicked_piece_index = self.game_logic.check_hovered_piece()
                    if clicked_piece_index is not None:
                        if self.game_logic.selected_piece_index is None:
                            if self.game_draw.board[clicked_piece_index] == self.current_player:
                                self.game_logic.selected_piece_index = clicked_piece_index
                                if not self.game_logic.check_blocked_piece(
                                        self.game_logic.selected_piece_index):
                                    self.game_logic.highlight_possible_moves(clicked_piece_index, self.current_player)
                        else:
                            if clicked_piece_index in self.game_logic.highlighted_hexagons:
                                if (self.current_player == 1 and clicked_piece_index != 26) or \
                                        (self.current_player == -1 and clicked_piece_index != 34):
                                    self.game_logic.move_piece(self.game_logic.selected_piece_index,
                                                               clicked_piece_index)
                                    self.current_player = -self.current_player  # Switch turns after a move
                            else:
                                self.game_logic.selected_piece_index = None
                                self.game_logic.highlighted_hexagons = []
                    else:
                        self.game_logic.selected_piece_index = None
                        self.game_logic.highlighted_hexagons = []

            self.game_draw.screen.fill(self.game_draw.colors["WHITE"])
            self.game_draw.draw_board()
            self.game_logic.highlight()
            self.game_draw.print_player_turn(self.current_player)
            pygame.display.flip()

            # Check for endgame conditions
            if self.game_draw.board[34] == 1:
                self.game_draw.print_player_wins(1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board[26] == -1:
                self.game_draw.print_player_wins(-1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(-1) == 0:
                self.game_draw.print_player_wins(1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(1) == 0:
                self.game_draw.print_player_wins(-1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(1) + self.game_draw.board.count(-1) == self.game_logic.count_blocked_pieces()[
                0] + self.game_logic.count_blocked_pieces()[1]:
                if self.game_draw.board.count(1) > self.game_draw.board.count(-1):
                    self.game_draw.print_player_wins(1)
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
                elif self.game_draw.board.count(1) < self.game_draw.board.count(-1):
                    self.game_draw.print_player_wins(-1)
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
                else:
                    self.game_draw.print_draw()
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
        pygame.quit()
        sys.exit()

    # This function executes a single game of Human vs CPU with the passed depth for player red
    def play_human_vs_computer(self, minimax_depth):
        self.game_logic.reset_board()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.menu()
                if self.current_player == -1:
                    time.sleep(0.25)
                    best_score, best_move = self.game_logic.minimax(minimax_depth, float('-inf'), float('inf'),
                                                                    self.current_player, True)
                    # print(f"\nMOVE PICKED BY PLAYER {self.current_player}: {best_move}\n")
                    if best_move is None:
                        self.current_player = -self.current_player
                        continue
                    self.game_logic.move_piece(best_move[0], best_move[1])
                    self.current_player = -self.current_player  # Switch turns after a move
                else:
                    if self.game_logic.count_blocked_pieces()[0] == self.game_draw.board.count(1):
                        self.current_player = -self.current_player
                        continue
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                        clicked_piece_index = self.game_logic.check_hovered_piece()
                        if clicked_piece_index is not None:
                            if self.game_logic.selected_piece_index is None:
                                if self.game_draw.board[clicked_piece_index] == self.current_player:
                                    self.game_logic.selected_piece_index = clicked_piece_index
                                    if not self.game_logic.check_blocked_piece(
                                            self.game_logic.selected_piece_index):
                                        self.game_logic.highlight_possible_moves(clicked_piece_index,
                                                                                 self.current_player)
                            else:
                                if clicked_piece_index in self.game_logic.highlighted_hexagons:
                                    if (self.current_player == 1 and clicked_piece_index != 26) or \
                                            (self.current_player == -1 and clicked_piece_index != 34):
                                        self.game_logic.move_piece(self.game_logic.selected_piece_index,
                                                                   clicked_piece_index)
                                        self.current_player = -self.current_player  # Switch turns after a move
                                else:
                                    self.game_logic.selected_piece_index = None
                                    self.game_logic.highlighted_hexagons = []
                        else:
                            self.game_logic.selected_piece_index = None
                            self.game_logic.highlighted_hexagons = []

            self.game_draw.screen.fill(self.game_draw.colors["WHITE"])
            self.game_draw.draw_board()
            self.game_logic.highlight()
            self.game_draw.print_player_turn(self.current_player)
            pygame.display.flip()

            # Check for endgame conditions
            if self.game_draw.board[34] == 1:
                self.game_draw.print_player_wins(1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board[26] == -1:
                self.game_draw.print_player_wins(-1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(-1) == 0:
                self.game_draw.print_player_wins(1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(1) == 0:
                self.game_draw.print_player_wins(-1)
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(1) + self.game_draw.board.count(-1) == self.game_logic.count_blocked_pieces()[
                0] + self.game_logic.count_blocked_pieces()[1]:
                if self.game_draw.board.count(1) > self.game_draw.board.count(-1):
                    self.game_draw.print_player_wins(1)
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
                elif self.game_draw.board.count(1) < self.game_draw.board.count(-1):
                    self.game_draw.print_player_wins(-1)
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
                else:
                    self.game_draw.print_draw()
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
        pygame.quit()
        sys.exit()

    # This function executes a single game of CPU vs CPU with the passed depths for each player
    def play_computer_vs_computer(self, minimax_depth_blue, minimax_depth_red):
        blue_win, red_win, draw = False, False, False
        blue_move_counter, red_move_counter = 0, 0
        blue_time, red_time = 0, 0
        self.game_logic.reset_board()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.menu()

            if self.current_player == 1:
                time.sleep(0.25)
                start_time = time.time()
                best_score, best_move = self.game_logic.minimax(minimax_depth_blue, float('-inf'), float('inf'),
                                                                self.current_player, True)
                end_time = time.time()
                blue_time += end_time - start_time
                # print(f"\nMOVE PICKED BY PLAYER {self.current_player}: {best_move}\n")
                if best_move is None:
                    self.current_player = -self.current_player
                    continue

                blue_move_counter += 1
                self.game_logic.move_piece(best_move[0], best_move[1])
                self.current_player = -self.current_player
            else:
                time.sleep(0.25) # Comment this delay if testing multiple games
                start_time = time.time()
                best_score, best_move = self.game_logic.minimax(minimax_depth_red, float('-inf'), float('inf'),
                                                                self.current_player, True)
                end_time = time.time()
                red_time += end_time - start_time
                # print(f"\nMOVE PICKED BY PLAYER {self.current_player}: {best_move}\n")
                if best_move is None:
                    self.current_player = -self.current_player
                    continue
                red_move_counter += 1
                self.game_logic.move_piece(best_move[0], best_move[1])
                self.current_player = -self.current_player

            self.game_draw.screen.fill(self.game_draw.colors["WHITE"])
            self.game_draw.draw_board()
            self.game_logic.highlight()
            self.game_draw.print_player_turn(self.current_player)
            pygame.display.flip()

            # Check for endgame conditions
            if self.game_draw.board[34] == 1:
                self.game_draw.print_player_wins(1)
                blue_win = True
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board[26] == -1:
                self.game_draw.print_player_wins(-1)
                red_win = True
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(-1) == 0:
                self.game_draw.print_player_wins(1)
                blue_win = True
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(1) == 0:
                self.game_draw.print_player_wins(-1)
                red_win = True
                pygame.display.flip()
                time.sleep(3)
                running = False
            if self.game_draw.board.count(1) + self.game_draw.board.count(-1) == self.game_logic.count_blocked_pieces()[
                0] + self.game_logic.count_blocked_pieces()[1]:
                if self.game_draw.board.count(1) > self.game_draw.board.count(-1):
                    self.game_draw.print_player_wins(1)
                    blue_win = True
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
                elif self.game_draw.board.count(1) < self.game_draw.board.count(-1):
                    self.game_draw.print_player_wins(-1)
                    red_win = True
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
                else:
                    self.game_draw.print_draw()
                    draw = True
                    pygame.display.flip()
                    time.sleep(3)
                    running = False
        return blue_win, red_win, draw, blue_move_counter, red_move_counter, blue_time, red_time

    # This function executes N number of CPU vs CPU games with the passed depths for each player
    def run_N_games_computer_vs_computer(self, n, depth_blue, depth_red):
        blue_wins = 0
        red_wins = 0
        draws = 0
        total_blue_moves, total_red_moves = 0, 0
        total_blue_time, total_red_time = 0, 0
        start_time = time.time()
        for i in range(n):
            b, r, d, b_m, r_m, b_t, r_t = self.play_computer_vs_computer(depth_blue, depth_red)
            blue_wins += b
            red_wins += r
            draws += d
            total_blue_moves += b_m
            total_red_moves += r_m
            total_blue_time += b_t
            total_red_time += r_t
        end_time = time.time()
        execution_time = end_time - start_time

        print(f"\nStatistics for {n} games of Blue CPU (depth {depth_blue}) vs Red CPU (depth {depth_red}):")
        print(f"Blue victories: {blue_wins} ({(blue_wins / n) * 100:.2f}%)")
        print(f"Red victories: {red_wins} ({(red_wins / n) * 100:.2f}%)")
        print(f"Draws: {draws} ({(draws / n) * 100:.2f}%)")
        print(f"Total execution time: {execution_time:.5f}s / Average per game: {execution_time / n:.5f}s")
        print(f"Average execution time per Blue move: {total_blue_time / total_blue_moves:.5f}s / per Red move: {total_red_time / total_red_moves:.5f}s\n")

        self.game_draw.display_results(blue_wins, red_wins, draws, n, depth_blue, depth_red)
        time.sleep(10) # Time showing the results, adjust by personal preference
