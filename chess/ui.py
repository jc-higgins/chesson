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
    for row in range(8):
        for col in range(8):
            colour = "white" if ((row + col)%2==0) else "#A9A9A9"
            pygame.draw.rect(screen, colour, pygame.Rect(((50+50*col), (50+50*row)),(50, 50)))
    
    # Pieces
    for row in range(8):
        for col in range(8):
            piece = game.board.board[row][col]
            if piece != '.':
                piece_img = PIECES[piece]
                # Calculate exact center position
                x = 50 + 50*col + (SQUARE_SIZE - PIECE_SIZE)//2
                y = 50 + 50*row + (SQUARE_SIZE - PIECE_SIZE)//2
                screen.blit(piece_img, (x, y))
    
    # Coordinates
    for row in range(8):
        text = font.render(str(8-row), True, "black")
        screen.blit(text, (40, 88+50*row))
    
    for col in range(8):
        text = font.render(chr(97+col), True, "black")
        screen.blit(text, (50+50*col, 451))

    # flip() the display to show rendered work
    pygame.display.flip()

    clock.tick(60)  # Limits FPS to 60

pygame.quit()