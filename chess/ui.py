from typing import Optional
import pygame

from chess.constants import JetBrainsMono, PIECES_DIR
from chess.game import Game
from chess.position import Position

# PyGame setup
pygame.init()
pygame.font.init()
font = pygame.font.Font(JetBrainsMono, 10)
screen = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()
running = True

# Initialize game
game = Game()

# Load and scale piece images
PIECES = {}
SQUARE_SIZE = 50
PIECE_SIZE = SQUARE_SIZE - 5  # Piece size slightly smaller than square

# Colours
LIGHT_SQUARE = "white"
DARK_SQUARE = "#A9A9A9"
SELECTED_COLOUR = "#646464"
HIGHLIGHT_COLOUR = "#FF474C"

# Game State
selected_square: Optional[Position] = None
legal_moves: list[Position] = []

def get_square_from_mouse(pos: tuple[int, int]) -> Optional[Position]:
    """
    Get the square from the mouse position.
    Args:
        pos: The position of the mouse, fed in from PyGame
    Returns:
        The square from the mouse position.
        None if the mouse is not on the board.
    """
    x, y = pos
    if not (50 <= x <= 450 and 50 <= y <= 450):
        return None

    col = (x) // SQUARE_SIZE
    row = 9 - ((y) // SQUARE_SIZE)
    print(row, col)
    if col < 1 or col > 8 or row < 1 or row > 8:
        return None
    return game.board.get_position(row, col)


for piece_type, filename in {
    # Black pieces (lowercase)
    'r': "rdt.png", 'n': "ndt.png", 'b': "bdt.png",
    'q': "qdt.png", 'k': "kdt.png", 'p': "pdt.png",
    # White pieces (uppercase)
    'R': "rlt.png", 'N': "nlt.png", 'B': "blt.png",
    'Q': "qlt.png", 'K': "klt.png", 'P': "plt.png",
}.items():
    # Load image
    piece_img = pygame.image.load(PIECES_DIR / filename)
    # Scale with smooth scaling for better quality
    PIECES[piece_type] = pygame.transform.smoothscale(piece_img, (PIECE_SIZE, PIECE_SIZE))

while running:
    # poll for events
    # pygame.QUIT event means user hit the X button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked_square = get_square_from_mouse(event.pos)
                print(f"{clicked_square=} {selected_square=}")
                if clicked_square:
                    # If selecting the same square, deselect it
                    if clicked_square == selected_square or clicked_square.piece == '.':
                        selected_square = None
                        legal_moves = []

                    # If selecting a legal move, make the move
                    elif clicked_square in legal_moves:
                        game.make_move(selected_square, clicked_square)
                        selected_square = None

                    # If selecting a piece, select it and update the legal moves
                    elif clicked_square.piece != '.':
                        selected_square = clicked_square
                        legal_moves = game.get_legal_moves(selected_square)


    # Clear the frame
    screen.fill("grey")

    # RENDER YOUR GAME HERE
    # Vertical Lines
    pygame.draw.line(screen, "black", (48, 48), (48, 450), width=2)
    pygame.draw.line(screen, "black", (450, 48), (450, 450), width=2)
    
    # Horizontal Lines
    pygame.draw.line(screen, "black", (48, 48), (450, 48), width=2)
    pygame.draw.line(screen, "black", (48, 450), (450, 450), width=2)

    # Squares
    for row in range(1, 9):
        for col in range(1, 9):
            colour = "white" if ((row + col)%2==0) else "#A9A9A9"
            y = 50 * (9 - row)
            pygame.draw.rect(screen, colour, pygame.Rect((50*col, y), (50, 50)))
    
    # Selected Square
    if selected_square:
        row, col = selected_square.row, selected_square.col
        y = 50 * (9 - row)
        pygame.draw.rect(screen, SELECTED_COLOUR, pygame.Rect((50*col, y), (50, 50)))
        for move in legal_moves:
            y_move = 50 * (9 - move.row)
            pygame.draw.rect(screen, HIGHLIGHT_COLOUR, pygame.Rect((50*move.col, y_move), (50, 50)))

    # Pieces
    for row in range(1, 9):
        for col in range(1, 9):
            piece = game.board.board[8-row][col-1]
            if piece != '.':
                piece_img = PIECES[piece]
                x = 50*col + (SQUARE_SIZE - PIECE_SIZE)//2
                y = 50 * (9 - row) + (SQUARE_SIZE - PIECE_SIZE)//2
                screen.blit(piece_img, (x, y))
    
    # Coordinates
    for row in range(1, 9):
        y = 38 + 50 * (9 - row)
        text = font.render(str(row), True, "black")
        screen.blit(text, (40, y))
    
    for col in range(1, 9):
        x = 50*col
        text = font.render(chr(47+col), True, "black")
        screen.blit(text, (x, 451))

    # flip() the display to show rendered work
    pygame.display.flip()

    clock.tick(60)  # Limits FPS to 60

pygame.quit()