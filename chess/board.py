

from typing import Literal, Optional, Union

from chess.constants import EMPTY, PIECE
from chess.fen import STARTING_FEN_STR, Fen
from chess.position import Position
from chess.pieces import (
    Pawn,
    Rook,
    Knight,
    Bishop,
    King,
    Queen,
    Empty
)
from chess.pieces import (
    Pawn,
    Rook,
    Knight,
    Bishop,
    King,
    Queen,
    Empty
)


class Board:
    board: list[list[PIECE]]

    def __init__(self, fen: Optional[Fen] = None):
        self.piece_key = {
            "p": Pawn(-1),
            "P": Pawn(1),
            "r": Rook(-1),
            "R": Rook(1),
            "n": Knight(-1),
            "N": Knight(1),
            "b": Bishop(-1),
            "B": Bishop(1),
            "q": Queen(-1),
            "Q": Queen(1),
            "k": King(-1),
            "K": King(1),
        }
        self.piece_key = {
            "p": Pawn(-1),
            "P": Pawn(1),
            "r": Rook(-1),
            "R": Rook(1),
            "n": Knight(-1),
            "N": Knight(1),
            "b": Bishop(-1),
            "B": Bishop(1),
            "q": Queen(-1),
            "Q": Queen(1),
            "k": King(-1),
            "K": King(1),
        }
        if fen:
            self.load_fen(fen)
        else:
            self.load_start_position()

    def _get_piece(self, pos: Position) -> Union[PIECE, EMPTY]:
        print(f"Asking for {pos.row} {pos.col}")
        if pos.is_impossible():
            return EMPTY
        return self.board[pos.y][pos.x]

    def get_position(self, row: int, col: int) -> Position:
        pos = Position(row, col)
        pos.piece = self._get_piece(pos)
        return pos 
    
    def load_start_position(self):
        self.load_fen(Fen(STARTING_FEN_STR))

    def load_fen(self, fen: Fen) -> None:
        # TODO: Validate FEN
        board = []
        for tokens in fen.get_board_str().split('/'):
            row = []
            for token in tokens:
                if token.isnumeric():
                    row += [Empty()] * int(token)
                    row += [Empty()] * int(token)
                else:
                    row.append(self.piece_key[token])
                    row.append(self.piece_key[token])
            board.append(row)
        self.board = board

    def __str__(self) -> str:
        s = "========\n"
        for row in self.board:
            print(row)
            s += ''.join([piece.piece_str for piece in row]) + '\n'
        s += "========"
        return s
    
    def change_piece_in_location(self, pos: Position):
        self.board[pos.y][pos.x] = pos.piece

if __name__ == "__main__":
    board = Board()
    print(board)