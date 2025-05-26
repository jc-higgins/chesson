from abc import abstractmethod
from chess.constants import POSITION
from abc import abstractmethod
from chess.constants import POSITION


class Piece:
    colour: int
    piece_str: str
    colour: int
    piece_str: str

    def __init__(self, colour: int):
        self.colour = colour
        if colour == 1:
            self.func = lambda x: x.upper()
        elif colour == -1:
            self.func = lambda x: x.lower()

    @abstractmethod
    def get_legal_moves(self, board, pos: POSITION) -> list[POSITION]: ...


    @abstractmethod
    def get_legal_moves(self, board, pos: POSITION) -> list[POSITION]: ...


class Knight(Piece):

    def __init__(self, colour):
        super().__init__(colour)
        self.piece_str = self.func("n")
        self.name = "Knight"
        self.value = 3



class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.piece_str = self.func("p")
        self.name = "Pawn"
        self.value = 1


class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.piece_str = self.func("r")
        self.name = "Rook"
        self.value = 5


class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.piece_str = self.func("b")
        self.name = "Bishop"
        self.value = 3



class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.piece_str = self.func("q")
        self.name = "Queen"
        self.value = 9



class King(Piece):
    def __init__(self, colour):
        super().__init__(colour)
        self.piece_str = self.func("k")
        self.name = "King"
        self.value = 100


class Empty(Piece):

class Empty(Piece):
    def __init__(self):
        self.colour = 0
        self.piece_str = "."
        self.name = "Empty"
        self.value = 0
