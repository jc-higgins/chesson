class Piece:
    colour: int
    piece_str: str
    name: str
    value: int = 0

    def __init__(self, colour: int, piece_str: str = ".") -> None:
        self.colour = colour
        self.piece_str = piece_str
        self.name = self.matched_piece(piece_str) if piece_str != "." else "Empty"
        self.value = 0

    def matched_piece(self, x: str) -> str:
        return x.upper() if self.colour == 1 else x.lower()


class Knight(Piece):
    name: str = "Knight"
    value: int = 3

    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("n") if colour == 1 else str.lower("n")
        )


class Pawn(Piece):
    name: str = "Pawn"
    value: int = 1

    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("p") if colour == 1 else str.lower("p")
        )


class Rook(Piece):
    name: str = "Rook"
    value: int = 5

    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("r") if colour == 1 else str.lower("r")
        )


class Bishop(Piece):
    name: str = "Bishop"
    value: int = 3

    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("b") if colour == 1 else str.lower("b")
        )


class Queen(Piece):
    name: str = "Queen"
    value: int = 9

    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("q") if colour == 1 else str.lower("q")
        )


class King(Piece):
    name: str = "King"
    value: int = 100

    def __init__(self, colour: int) -> None:
        super().__init__(
            colour=colour, piece_str=str.upper("k") if colour == 1 else str.lower("k")
        )


class Empty(Piece):
    name: str = "Empty"
    value: int = 0

    def __init__(self) -> None:
        super().__init__(colour=0, piece_str=".")
