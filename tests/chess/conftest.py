
import pytest
from chess.game import Game
from chess.fen import Fen


@pytest.fixture
def starting_fen() -> Fen:
    return Fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


@pytest.fixture
def starting_game(starting_fen: str) -> Game:
    return Game(starting_fen)
