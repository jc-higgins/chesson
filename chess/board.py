

from typing import Literal


class Board:
    board: list[list[Literal['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']]]

    def __init__(self, fen: str=None):
        if fen:
            self.load_fen(fen)
        else:
            self.load_start_position()

    def load_start_position(self):
        self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def load_fen(self, fen: str) -> None:
        # TODO: Validate FEN
        board = []
        for tokens in fen.split(' ')[0].split('/'):
            row = []
            for token in tokens:
                if token.isnumeric():
                    row += ['.'] * int(token)
                else:
                    row.append(token)
            board.append(row)
        self.board = board
        print(self.board)


    def __str__(self) -> str:
        s = "========\n"
        for row in self.board:
            s += ''.join(row) + '\n'
        s += "========"
        return s

if __name__ == "__main__":
    board = Board()
    print(board)