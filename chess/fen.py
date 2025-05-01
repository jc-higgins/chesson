

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Fen:
    def __init__(self, fen: str = STARTING_FEN):
        self.fen = fen

    def get_board_str(self) -> str:
        return self.fen.split()[0]

    def get_turn(self) -> str:
        return self.fen.split()[1]
    
    def get_castles(self) -> str:
        return self.fen.split()[2]
    
    def get_en_passant(self) -> str:
        return self.fen.split()[3]
    
    def get_halfmove_clock(self) -> str:
        return self.fen.split()[4]
    
    def get_fullmove_number(self) -> str:
        return self.fen.split()[5]
    
    