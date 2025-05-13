from pathlib import Path
from typing import Literal

PIECE = Literal['p', 'r', 'n', 'b', 'q', 'k', 'P', 'R', 'N', 'B', 'Q', 'K']
EMPTY = Literal['.']

# Get the directory where constants.py is located
ASSETS = Path(__file__).parent / "assets"

# Font paths
JetBrainsMono = ASSETS / "fonts" / "JetBrainsMono-Regular.ttf"

# Piece paths
PIECES_DIR = ASSETS / "pieces"