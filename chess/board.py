import logging
from typing import Literal, Optional, Union

from chess.constants import EMPTY, PIECE
from chess.fen import STARTING_FEN_STR, Fen
from chess.pieces import (
    Pawn,
    Piece,
    Rook,
    Knight,
    Bishop,
    King,
    Queen,
    Empty
)


class Board:
    board: list[list[Union[Piece, EMPTY]]]
    piece_key: dict[str, PIECE]

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
            ".": Empty()
        }
        if fen:
            self.load_fen(fen)
        else:
            self.load_start_position()

    def _get_piece(self, pos: Position) -> Union[PIECE, EMPTY]:
        if pos.is_impossible():
            return EMPTY
        return self.board[pos.y][pos.x]

    def is_impossible(self, col: int, row: int) -> bool:
        if row > 8 or row < 1 or col > 8 or col < 1:
            return True
        return False
    
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
                else:
                    piece = self.piece_key[token]
                    logging.info(f"Loading piece {token} with colour {piece.colour}")
                    row.append(piece)
            board.append(row)
        self.board = board

    def __str__(self) -> str:
        s = "========\n"
        for row in self.board:
            s += ''.join([piece.piece_str for piece in row]) + '\n'
        s += "========"
        return s
    
    def change_piece_in_location(self, row: int, col: int, piece: Piece):
        self.board[row-1][col-1] = piece

if __name__ == "__main__":
    board = Board()
    print(board)