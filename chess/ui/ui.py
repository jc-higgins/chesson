# ======= IMPORTS =======
import logging
from typing import Optional
import pygame

from chess.constants import EMPTY, JetBrainsMono, PIECES_DIR, POSITION
from chess.game import Game
from chess.pieces import Empty
from chess.pieces import Empty
from chess.ui.ui_constants import HIGHLIGHT_COLOUR, PIECE_SIZE, SELECTED_COLOUR, SQUARE_SIZE


class UI:
    clock: pygame.time.Clock
    font: pygame.font.Font
    game: Game
    legal_moves: list[POSITION]
    legal_moves: list[POSITION]
    piece_images: dict[str, pygame.Surface]
    running: bool
    screen: pygame.Surface
    selected_square: Optional[POSITION]
    selected_square: Optional[POSITION]

    def __init__(self) -> None:
        # ======= VARIABLES SETUP =======
        # PyGame setup
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.Font(JetBrainsMono, 10)
        self.screen = pygame.display.set_mode((500,500))
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game
        self.game = Game()

        # Game State
        self.selected_square = None
        self.legal_moves = []

        # Load piece images
        self.piece_images = {}
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
            self.piece_images[piece_type] = pygame.transform.smoothscale(piece_img, (PIECE_SIZE, PIECE_SIZE))
            

    # ======= SUPPORTING FUNCTIONS =======
    def get_square_from_mouse(self, pos: tuple[int, int]) -> Optional[POSITION]:
    def get_square_from_mouse(self, pos: tuple[int, int]) -> Optional[POSITION]:
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
        if col < 1 or col > 8 or row < 1 or row > 8:
            return None
        return (col, row)


    def handle_mouse_click(self, event: pygame.event.Event) -> None:
        if event.button == 1:
            clicked_square = self.get_square_from_mouse(event.pos)
            if clicked_square:
                # If selecting the same square, deselect it
                if clicked_square == self.selected_square or self.game.board._get_piece(*clicked_square).piece_str == '.':
                    self.selected_square = None
                    self.legal_moves = []

                # If selecting a legal move, make the move
                elif clicked_square in self.legal_moves:
                    print(f"Selected legal move, piece is {clicked_piece}")
                    self.game.make_move(self.selected_square, clicked_square)
                    self.selected_square = None

                # If selecting a piece, select it and update the legal moves
                elif self.game.board._get_piece(*clicked_square).piece_str != '.':
                    if self.game.piece_matches_player(self.game.board._get_piece(*clicked_square)):
                        self.selected_square = clicked_square
                        self.legal_moves = self.game.get_legal_moves(self.selected_square)
                        self.legal_moves = self.game.get_legal_moves(self.selected_square)


    # ======= MAIN GAME LOOP =======
    def run(self) -> None:
        while self.running:
            # poll for events
            # pygame.QUIT event means user hit the X button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)

            # Clear the frame
            self.screen.fill("grey")

            # Vertical Lines
            pygame.draw.line(self.screen, "black", (48, 48), (48, 450), width=2)
            pygame.draw.line(self.screen, "black", (450, 48), (450, 450), width=2)
            
            # Horizontal Lines
            pygame.draw.line(self.screen, "black", (48, 48), (450, 48), width=2)
            pygame.draw.line(self.screen, "black", (48, 450), (450, 450), width=2)

            # Squares
            for row in range(1, 9):
                for col in range(1, 9):
                    colour = "white" if ((row + col)%2==0) else "#A9A9A9"
                    y = 50 * (9 - row)
                    pygame.draw.rect(self.screen, colour, pygame.Rect((50*col, y), (50, 50)))
            
            # Selected Square
            if self.selected_square:
                col, row = self.selected_square
                y = 50 * (9 - row)
                pygame.draw.rect(self.screen, SELECTED_COLOUR, pygame.Rect((50*col, y), (50, 50)))
                for move in self.legal_moves:
                    col, row = move
                    y_move = 50 * (9 - row)
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOUR, pygame.Rect((50*col, y_move), (50, 50)))

            # Pieces
            for row in range(1, 9):
                for col in range(1, 9):
                    piece = self.game.board.get_piece(col, row)
                    if not isinstance(piece, Empty):
                        piece_img = self.piece_images[piece.piece_str]
                        x = 50*col + (SQUARE_SIZE - PIECE_SIZE)//2
                        y = 50 * (9 - row) + (SQUARE_SIZE - PIECE_SIZE)//2
                        self.screen.blit(piece_img, (x, y))

            # Coordinates
            for row in range(1, 9):
                y = 38 + 50 * (9 - row)
                text = self.font.render(str(row), True, "black")
                self.screen.blit(text, (40, y))
            
            for col in range(1, 9):
                x = 50*col
                text = self.font.render(chr(47+col), True, "black")
                self.screen.blit(text, (x, 451))

            # flip() the display to show rendered work
            pygame.display.flip()

            self.clock.tick(60)  # Limits FPS to 60

        pygame.quit()


if __name__ == "__main__":
    ui = UI()
    ui.run()