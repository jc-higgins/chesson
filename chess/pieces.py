from abc import abstractmethod
from chess.constants import POSITION


class Piece:
    colour: int
    piece_str: str

    def __init__(self, colour: int):
        self.colour = colour
        if colour == 1:
            self.func = lambda x: x.upper()
        elif colour == -1:
            self.func = lambda x: x.lower()

    @abstractmethod
    def get_legal_moves(self, board, pos: POSITION) -> list[POSITION]:
        ...


class Knight(Piece):

    def __init__(self, colour):
        super().__init__( colour)
        self.piece_str = self.func("n")

    def get_legal_moves(self, board, pos: POSITION):
        row, col = pos
        legal_moves: list[POSITION] = []
        possible_moves = [
            (row+2, col+1),
            (row+2, col-1),
            (row-2, col+1),
            (row-2, col-1),
            (row+1, col+2),
            (row+1, col-2),
            (row-1, col+2),
            (row-1, col-2),
        ]
        
        for square in possible_moves:
            if board.is_impossible(*square):
                continue
            piece = board.get_piece(*square)
            if piece.colour == self.colour:
                continue
            else:
                legal_moves.append(square)
        return legal_moves


class Pawn(Piece):
    def __init__(self, colour):
        super().__init__( colour)
        self.piece_str = self.func("p")

    def get_legal_moves(self, board, pos: POSITION):
        row, col = pos
        legal_moves = []
        square_1 = (row+self.colour, col)
        square_2 = (row+2*self.colour, col)

        if not board.is_impossible(*square_1) and board.get_piece(*square_1).piece_str == ".":
            legal_moves.append(square_1)
            if not board.is_impossible(*square_2) and board.get_piece(*square_2).piece_str == "." and 2*row ==  (9-5*self.colour):
                legal_moves.append(square_2)

        attack_squares = [(row+self.colour, col+1), (row+self.colour, col-1)]
        for square in attack_squares:
            if not board.is_impossible(*square) and board.get_piece(*square).colour == -self.colour:
                legal_moves.append(square)
            


        return legal_moves
    

class Rook(Piece):
    def __init__(self, colour):
        super().__init__( colour)
        self.piece_str = self.func("r")

    def get_legal_moves(self, board, pos: POSITION):
        row, col = pos
        legal_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = (row+steps*dir[0], col+steps*dir[1])
                if board.is_impossible(*square):
                    break
                piece = board.get_piece(*square)
                if piece.colour == self.colour:
                    break
                elif piece.colour == -self.colour:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves


class Bishop(Piece):
    def __init__(self, colour):
        super().__init__( colour)
        self.piece_str = self.func("b")

    def get_legal_moves(self, board, pos: POSITION):
        row, col = pos
        legal_moves = []

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = (row+steps*dir[0], col+steps*dir[1])
                if board.is_impossible(*square):
                    break
                piece = board.get_piece(*square)
                if piece.colour == self.colour:
                    break
                elif piece.colour == -self.colour:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves


class Queen(Piece):
    def __init__(self, colour):
        super().__init__( colour)
        self.piece_str = self.func("q")
    
    def get_legal_moves(self, board, pos: POSITION):
        row, col = pos
        legal_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = (row+steps*dir[0], col+steps*dir[1])
                if board.is_impossible(*square):
                    break
                piece = board.get_piece(*square)
                if piece.colour == self.colour:
                    break
                elif piece.colour == -self.colour:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves


class King(Piece):
    def __init__(self, colour):
        super().__init__( colour)
        self.piece_str = self.func("k")

    def get_legal_moves(self, board, pos: POSITION):
        row, col = pos
        legal_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            square = (row+dir[0], col+dir[1])
            if board.is_impossible(*square):
                continue
            piece = board.get_piece(*square)
            if piece.colour == self.colour:
                continue
            elif piece.colour == -self.colour:
                legal_moves.append(square)
                continue
            else:
                legal_moves.append(square)

        return legal_moves


class Empty(Piece):
    def __init__(self):
        self.colour = 0
        self.piece_str = "."