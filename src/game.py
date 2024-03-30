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
                            self.play_computer_vs_computer(1)
                        elif event.key == pygame.K_2:
                            self.play_computer_vs_computer(2)
                        elif event.key == pygame.K_3:
                            self.play_computer_vs_computer(3)

            self.game_draw.screen.fill(self.game_draw.colors["WHITE"])
            self.game_draw.print_menu_difficulty()
            pygame.display.flip()

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
                    best_score, best_move = self.game_logic.minimax(minimax_depth, float('-inf'), float('inf'), self.current_player, True)
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

    def play_computer_vs_computer(self, minimax_depth):
        self.game_logic.reset_board()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            time.sleep(0.5)
            best_score, best_move = self.game_logic.minimax(minimax_depth, float('-inf'), float('inf'), self.current_player, True)
            if best_move is None:
                self.current_player = -self.current_player
                continue
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
