

from typing import Literal, Optional, Union

from chess.constants import EMPTY, PIECE
from chess.fen import STARTING_FEN_STR, Fen
from chess.position import Position


class Board:
    board: list[list[PIECE]]

    def __init__(self, fen: Optional[Fen] = None):
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
                    row += ['.'] * int(token)
                else:
                    row.append(token)
            board.append(row)
        self.board = board

    def __str__(self) -> str:
        s = "========\n"
        for row in self.board:
            s += ''.join(row) + '\n'
        s += "========"
        return s
    
    def change_piece_in_location(self, pos: Position):
        self.board[8-pos.row][pos.col-1] = pos.piece

if __name__ == "__main__":
    board = Board()
    print(board)