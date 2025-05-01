from chess.board import Board


class Game:
    def __init__(self, fen=None):
        self.board = Board(fen)
        self.turn = 'w' 
        self.turn = self.get_turn(fen)
        self.castles = self.starting_castles(fen)
        en_passant: 


if __name__ == "__main__":
    pass