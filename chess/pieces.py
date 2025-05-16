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
    
    def final_move_check(self, possible_moves: list[Position]):
        
        legal_moves: list[Position] = []
        for pos_move in possible_moves:
            if pos_move.is_impossible():
                continue
            if pos_move.piece.piece_str != ".":
                if pos_move.piece.colour == self.colour:
                    continue
            legal_moves.append(pos_move)
        return legal_moves

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
        
        return self.final_move_check(possible_moves)

class Pawn(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("p")

    def get_legal_moves(self, board, pos: Position):
        possible_moves: list[Position] = []
        row, col = pos.row, pos.col
        pawn_start_rank = int(4.5 - 5*self.colour/2)
        if row == pawn_start_rank:
            possible_moves.append(self.board.get_position(row+2*self.colour, col))
        possible_moves.append(self.board.get_position(row+1, col))
        
        # TODO: Add diagonal takes
        # TODO: Add en passant
        # TODO: Add promotion

        return self.final_move_check(possible_moves)
    

class Rook(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("r")

class Bishop(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("b")

class Queen(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("q")

class King(Piece):
    def __init__(self, colour):
        Piece.__init__(self, colour)
        self.piece_str = self.func("k")


class Empty:
    def __init__(self):
        self.colour = 0
        self.piece_str = "."