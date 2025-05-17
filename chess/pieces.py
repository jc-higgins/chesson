from typing import Literal, Optional, Union

from chess.constants import EMPTY, PIECE
from chess.fen import STARTING_FEN_STR, Fen
from chess.position import Position

class Piece:

    def __init__(self, colour: int):
        self.colour = colour
        if colour == 1:
            self.func = lambda x: x.upper()
        elif colour == -1:
            self.func = lambda x: x.lower()

class Knight(Piece):

    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("n")

    def get_legal_moves(self, board, pos: Position):
        row, col = pos.row, pos.col
        legal_moves: list[Position] = []
        possible_moves = [
            board.get_position(row+2, col+1),
            board.get_position(row+2, col-1),
            board.get_position(row-2, col+1),
            board.get_position(row-2, col-1),
            board.get_position(row+1, col+2),
            board.get_position(row+1, col-2),
            board.get_position(row-1, col+2),
            board.get_position(row-1, col-2),
        ]
        
        
        for square in possible_moves:
            if square.is_impossible():
                continue
            elif square.piece.colour == self.colour:
                continue
            else:
                legal_moves.append(square)
        return legal_moves

class Pawn(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("p")

    def get_legal_moves(self, board, pos: Position):
        row, col = pos.row, pos.col
        legal_moves = []
        square_1 = board.get_position(row+self.colour, col)
        square_2 = board.get_position(row+2*self.colour, col)

        if not square_1.is_impossible() and square_1.piece.piece_str == ".":
            legal_moves.append(square_1)
            if not square_2.is_impossible() and square_2.piece.piece_str == "." and 2*row ==  (9-5*self.colour):
                legal_moves.append(square_2)

        
        attack_squares = [board.get_position(row+self.colour, col+1), board.get_position(row+self.colour, col-1)]
        for square in attack_squares:
            if not square.is_impossible() and square.piece.colour == -self.colour:
                legal_moves.append(square)
            


        return legal_moves
    

class Rook(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("r")

    def get_legal_moves(self, board, pos: Position):
        row, col = pos.row, pos.col
        legal_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = board.get_position(row+steps*dir[0], col+steps*dir[1])
                if square.is_impossible():
                    break
                elif square.piece.colour == self.colour:
                    break
                elif square.piece.colour == -self.colour:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves


class Bishop(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("b")

    def get_legal_moves(self, board, pos: Position):
        row, col = pos.row, pos.col
        legal_moves = []

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = board.get_position(row+steps*dir[0], col+steps*dir[1])
                if square.is_impossible():
                    break
                elif square.piece.colour == self.colour:
                    break
                elif square.piece.colour == -self.colour:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves

class Queen(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("q")
    
    def get_legal_moves(self, board, pos: Position):
        row, col = pos.row, pos.col
        legal_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = board.get_position(row+steps*dir[0], col+steps*dir[1])
                if square.is_impossible():
                    break
                elif square.piece.colour == self.colour:
                    break
                elif square.piece.colour == -self.colour:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves

class King(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("k")

    def get_legal_moves(self, board, pos: Position):
        row, col = pos.row, pos.col
        legal_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            square = board.get_position(row+dir[0], col+dir[1])
            if square.is_impossible():
                continue
            elif square.piece.colour == self.colour:
                continue
            elif square.piece.colour == -self.colour:
                legal_moves.append(square)
                continue
            else:
                legal_moves.append(square)

        return legal_moves

class Empty:
    def __init__(self):
        self.colour = 0
        self.piece_str = "."