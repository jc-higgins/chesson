import pygame

from chess.constants import JetBrainsMono
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

# Dictionary for piece symbols (using Unicode chess pieces)
PIECES = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    '.': ' '
}

# Create a larger font for pieces
piece_font = pygame.font.SysFont('Arial', 40)  # Arial tends to have good Unicode support

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
            colour = "white" if ((row + col)%2==0) else "black"
            pygame.draw.rect(screen, colour, pygame.Rect(((50+50*col), (50+50*row)),(50, 50)))
    
    # Pieces
    for row in range(8):
        for col in range(8):
            piece = game.board.board[row][col]
            if piece != '.':
                text_color = "white" if piece.isupper() else "black"
                piece_text = piece_font.render(PIECES[piece], True, text_color)
                # Center the piece in the square
                text_rect = piece_text.get_rect(center=(75+50*col, 75+50*row))
                screen.blit(piece_text, text_rect)
    
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