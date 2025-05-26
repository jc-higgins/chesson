class Piece:
    colour: int
    piece_str: str
    name: str
    value: int = 0

    def __init__(self, colour: int, piece_str: str = ".") -> None:
        self.colour = colour
        self.piece_str = piece_str
        self.value = 0
        # Don't set name here, let the subclasses handle it

    def matched_piece(self, x: str) -> str:
        return x.upper() if self.colour == 1 else x.lower()


class Knight(Piece):
    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("n") if colour == 1 else str.lower("n")
        )
        self.name = "Knight"
        self.value = 3


class Pawn(Piece):
    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("p") if colour == 1 else str.lower("p")
        )
        self.name = "Pawn"
        self.value = 1


class Rook(Piece):
    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("r") if colour == 1 else str.lower("r")
        )
        self.name = "Rook"
        self.value = 5


class Bishop(Piece):
    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("b") if colour == 1 else str.lower("b")
        )
        self.name = "Bishop"
        self.value = 3


class Queen(Piece):
    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("q") if colour == 1 else str.lower("q")
        )
        self.name = "Queen"
        self.value = 9


class King(Piece):
    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("k") if colour == 1 else str.lower("k")
        )
        self.name = "King"
        self.value = 100


class Empty(Piece):
    def __init__(self) -> None:
        super().__init__(colour=0, piece_str=".")
        self.name = "Empty"
        self.value = 0
