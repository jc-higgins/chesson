import logging

import pytest

from chess.game import Game

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_board_setup_from_fen(starting_game: Game) -> None:
    print(starting_game.board)
    assert starting_game.board.board == [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]


def test_board_setup_from_fen_with_castles(starting_game: Game) -> None:
    assert starting_game.castles == "KQkq"


def test_board_setup_from_fen_with_en_passant(starting_game: Game) -> None:
    assert starting_game.en_passant == "-"


def test_board_setup_from_fen_with_halfmove_clock(starting_game: Game) -> None:
    assert starting_game.halfmove_clock == "0"


def test_board_setup_from_fen_with_fullmove_number(starting_game: Game) -> None:
    assert starting_game.fullmove_number == "1"


@pytest.mark.parametrize(
    "row, col, expected_moves",
    [
        (2, 2, [(4, 2), (3, 2)]),
        (1, 1, []),
        (1, 2, [(3, 1), (3, 3)]),
        (1, 3, []),
        (1, 4, []),
        (1, 5, []),
    ],
    ids=["pawn", "rook", "knight", "bishop", "queen", "king"],
)
def test_board_get_legal_moves(
    starting_game: Game, row: int, col: int, expected_moves: list[tuple[int, int]]
) -> None:
    assert set(starting_game.get_legal_moves(row, col)) == set(expected_moves)
