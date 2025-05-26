import logging
from typing import Optional, Union

from chess.fen import STARTING_FEN_STR, Fen
from chess.pieces import Bishop, Empty, King, Knight, Pawn, Piece, Queen, Rook


class Board:
    board: list[list[Union[Piece, Empty]]]
    piece_key: dict[str, Piece]

    def __init__(self, fen: Optional[Fen] = None) -> None:
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
            ".": Empty(),
        }
        if fen:
            self.load_fen(fen)
        else:
            self.load_start_position()

    def get_piece(self, row: int, col: int) -> Union[Piece, Empty]:
        if self.is_impossible(row, col):
            return Empty()
        return self.board[row - 1][col - 1]

    def is_impossible(self, col: int, row: int) -> bool:
        if row > 8 or row < 1 or col > 8 or col < 1:
            return True
        return False

    def load_start_position(self) -> None:
        self.load_fen(Fen(STARTING_FEN_STR))

    def load_fen(self, fen: Fen) -> None:
        # TODO: Validate FEN
        board: list[list[Union[Piece, Empty]]] = []
        for tokens in fen.get_board_str().split("/"):
            row: list[Union[Piece, Empty]] = []
            for token in tokens:
                if token.isnumeric():
                    row += [Empty()] * int(token)
                else:
                    piece = self.piece_key[token]
                    logging.info(f"Loading piece {token} with colour {piece.colour}")
                    row.append(piece)
            board.append(row)
        self.board = board[::-1]

    def __str__(self) -> str:
        s = ["========"]
        for row in self.board:
            s.append("".join([piece.piece_str for piece in row]))
        s.append("========")
        return "\n".join(s[::-1])

    def change_piece_in_location(self, row: int, col: int, piece: Piece) -> None:
        self.board[row - 1][col - 1] = piece


if __name__ == "__main__":
    board = Board()
    print(board)
