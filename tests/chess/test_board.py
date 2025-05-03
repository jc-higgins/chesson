

from chess.game import Game


def test_board_setup_from_fen(starting_game: Game):
    print(starting_game.board)
    assert starting_game.board.board == [
        ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
        ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
        ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ]


def test_board_setup_from_fen_with_castles(starting_game: Game):
    assert starting_game.castles == "KQkq"


def test_board_setup_from_fen_with_en_passant(starting_game: Game):
    assert starting_game.en_passant == "-"


def test_board_setup_from_fen_with_halfmove_clock(starting_game: Game):
    assert starting_game.halfmove_clock == "0"


def test_board_setup_from_fen_with_fullmove_number(starting_game: Game):
    assert starting_game.fullmove_number == "1"
