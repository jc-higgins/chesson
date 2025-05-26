import pytest

from chess.fen import Fen
from chess.game import Game


@pytest.fixture
def starting_fen() -> Fen:
    return Fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


@pytest.fixture
def starting_game() -> Game:
    return Game()
