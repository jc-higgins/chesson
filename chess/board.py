

from typing import Literal, Optional

from chess.fen import STARTING_FEN_STR, Fen


class Board:
    board: list[list[Literal['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']]]

    def __init__(self, fen: Optional[Fen] = None):
        if fen:
            self.load_fen(fen)
        else:
            self.load_start_position()

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

if __name__ == "__main__":
    board = Board()
    print(board)