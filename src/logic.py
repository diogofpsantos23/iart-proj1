import sys
import pygame


class GameLogic:
    def __init__(self, game_draw):
        self.game_draw = game_draw
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
        # Highlight hexagons where a move is possible
        # Here, you can implement your logic to determine possible moves for a piece
        # For now, let's highlight all hexagons except the current one
        for i in range(61):
            if i != piece_index and self.game_draw.board[i] == 0:
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
        self.place_piece(0, self.game_draw.colors["RED"])
        self.place_piece(1, self.game_draw.colors["BLUE"])
        running = True
        while running:
            print(self.game_draw.board)
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
            for hexagon_index in self.highlighted_hexagons:
                x, y = self.game_draw.hexagon_centers[hexagon_index]
                pygame.draw.circle(self.game_draw.screen, (0, 255, 0), (x, y), 10, width=10)
            pygame.display.flip()
        pygame.quit()
        sys.exit()
