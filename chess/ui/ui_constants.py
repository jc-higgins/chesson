# Load and scale piece images
from typing import Optional
from chess.position import Position

SQUARE_SIZE = 50
PIECE_SIZE = SQUARE_SIZE - 5  # Piece size slightly smaller than square

# Colours
LIGHT_SQUARE = "white"
DARK_SQUARE = "#A9A9A9"
SELECTED_COLOUR = "#646464"
HIGHLIGHT_COLOUR = "#FF474C"
