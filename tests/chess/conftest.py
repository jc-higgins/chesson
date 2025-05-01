
import pytest
from chess.game import Game



@pytest.fixture
def starting_fen() -> str:
    return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


@pytest.fixture
def starting_game(starting_fen: str) -> Game:
    return Game(starting_fen)