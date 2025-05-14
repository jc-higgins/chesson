from typing import Literal, Optional, Self, Union

from chess.constants import EMPTY, PIECE
from chess.fen import STARTING_FEN_STR, Fen


class Position:
    # Board Space
    _row: int
    _col: int

    # Python Dict Space
    _x: int
    _y: int

    _piece: Union[PIECE, EMPTY, None]

    def __init__(self, row: int, col: int, piece: Optional[PIECE] = None):
        self._row = row
        self._col = col
        self._x = col-1
        self._y = 8-row
        self._piece = piece 

    @property
    def row(self) -> int:
        return self._row

    @property
    def col(self) -> int:
        return self._col

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def piece(self) -> int:
        return self._piece

    @piece.setter
    def piece(self, piece: Union[PIECE, EMPTY]) -> None:
        self._piece = piece

    def is_impossible(self) -> bool:
        if self._row > 8 or self._row < 1 or self._col > 8 or self._col < 1:
            return True
        return False
    
    def __eq__(pos1: Self, pos2: Self) -> bool:
        if pos1 is None or pos2 is None:
            return False
        elif pos1.col == pos2.col and pos1.row == pos2.row:
            if pos1.piece and pos2.piece and pos1.piece != pos2.piece:
                return False
            else:
                return True
        return False