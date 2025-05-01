from typing import Optional
from chess.board import Board
from chess.fen import Fen


class Game:
    def __init__(self, fen: Optional[Fen] = None):
        self.board = Board(fen)
        self.turn = fen.get_turn()
        self.castles = fen.get_castles()
        self.en_passant = fen.get_en_passant()
        self.halfmove_clock = fen.get_halfmove_clock()
        self.fullmove_number = fen.get_fullmove_number()

if __name__ == "__main__":
    pass