from typing import Optional
import pygame

from chess.constants import JetBrainsMono, PIECES_DIR
from chess.game import Game

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
selected_square = None # (row, col)
legal_moves = []

def get_square_from_mouse(pos) -> Optional[tuple[str,str]]:
    x,y = pos
    if not (50 <= x <= 450 and 50 <= y <= 450):
        return None

    column = (x) // SQUARE_SIZE
    row = (y) // SQUARE_SIZE
    print(row, column)
    if column < 0 or column > 8 or row < 0 or row > 8:
        return None
    elif game.board.board[row-1][column-1] == '.':
        return None
    return row, column


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
                if clicked_square:
                    row, col = clicked_square
                    if selected_square == (row, col):
                        selected_square = None
                    elif game.board.board[row-1][col-1] != '.':
                        selected_square = (row, col)
                        legal_moves = game.get_legal_moves(row, col)
                    else:
                        selected_square = None
    
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
            pygame.draw.rect(screen, colour, pygame.Rect(((50*col), (50*row)),(50, 50)))
    
    # Selected Square
    if selected_square:
        row, col = selected_square
        pygame.draw.rect(screen, SELECTED_COLOUR, pygame.Rect(((50*col), (50*row)),(50, 50)))
        for move in legal_moves:
            pygame.draw.rect(screen, HIGHLIGHT_COLOUR, pygame.Rect(((50*move[1]), (50*move[0])),(50, 50)))

    # Pieces
    for row in range(1, 9):
        for col in range(1, 9):
            piece = game.board.board[row-1][col-1]
            if piece != '.':
                piece_img = PIECES[piece]
                # Calculate exact center position
                x = 50*col + (SQUARE_SIZE - PIECE_SIZE)//2
                y = 50*row + (SQUARE_SIZE - PIECE_SIZE)//2
                screen.blit(piece_img, (x, y))
    
    # Coordinates
    for row in range(1, 9):
        text = font.render(str(9-row), True, "black")
        screen.blit(text, (40, 38+50*row))
    
    for col in range(1, 9):
        text = font.render(chr(47+col), True, "black")
        screen.blit(text, (50*col, 451))

    # flip() the display to show rendered work
    pygame.display.flip()

    clock.tick(60)  # Limits FPS to 60

pygame.quit()