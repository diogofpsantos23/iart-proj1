from draw import GameDraw
from logic import GameLogic


class AboyneGame:
    def __init__(self):
        self.game_draw = GameDraw()
        self.game_logic = GameLogic(self.game_draw)

    def run(self):
        self.game_logic.game_loop()
