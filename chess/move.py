from chess.pieces import Piece
from typing import Literal, Optional, Union


class Move:
    def __init__(
        self,
        start_pos: tuple[int],
        end_pos: tuple[int],
        piece: Optional[Piece] = None,
        spaces: Optional[list[tuple[int]]] = None,
    ):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.piece = piece
        self.spaces = spaces
    
    def __eq__(self, other):
        start_pos_match = self.start_pos == other.start_pos
        end_pos_match = self.end_pos == other.end_pos
        piece_match = self.piece == other.piece if self.piece and other.piece else True

        return start_pos_match and end_pos_match and piece_match



