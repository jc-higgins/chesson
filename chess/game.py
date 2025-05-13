import logging
from typing import Optional
from chess.board import Board
from chess.fen import STARTING_FEN_STR, Fen
from chess.exceptions import TurnOrderError


class Game:
    def __init__(self, fen: Optional[Fen] = Fen(STARTING_FEN_STR)):
        self.board = Board(fen)
        self.turn = fen.get_turn()
        self.castles = fen.get_castles()
        self.en_passant = fen.get_en_passant()
        self.halfmove_clock = fen.get_halfmove_clock()
        self.fullmove_number = fen.get_fullmove_number()
        self.current_player = "w"

    def get_piece_locations(self, player):
        locations = []
        if player == "w":
            matches_upper = True
        else:
            matches_upper = False
        for row in range(1, 9):
            for col in range(1, 9):
                piece = self.board.board[8-row][col-1]
                if (piece == piece.upper()) == matches_upper and piece != '.':
                    locations.append([(row, col), piece])

        return locations

    def get_legal_moves(self, row: int, col: int) -> list[tuple[int, int]]:
        piece = self.board.board[8-row][col-1]
        logging.warning(f"Piece: {piece}")
        piece = piece.lower()
        match piece:
            case 'p':
                return self.get_legal_moves_for_pawn(row, col)
            case 'r':
                return self.get_legal_moves_for_rook(row, col)
            case 'n':
                return self.get_legal_moves_for_knight(row, col)
            case 'b':
                return self.get_legal_moves_for_bishop(row, col)
            case 'q':
                return self.get_legal_moves_for_queen(row, col)
            case 'k':
                return self.get_legal_moves_for_king(row, col)
            case '.':
                return []
            case _:
                logging.warning(f"No matching case for piece: {piece}")
                return []
            

    def get_legal_moves_for_pawn(self, row: int, col: int) -> list[tuple[int, int]]:
        legal_moves = []
        possible_moves = []
        if self.turn == 'w':
            if row == 2:
                possible_moves.append((row+2, col))
            possible_moves.append((row+1, col))
        else:
            if row == 7:
                possible_moves.append((row-2, col))
            possible_moves.append((row-1, col))
        
        for move in possible_moves:
            if move[0] < 1 or move[0] > 8 or move[1] < 1 or move[1] > 8:
                continue
            if self.board.board[8-move[0]][move[1]-1] != '.':
                continue
            legal_moves.append(move)
        return legal_moves
        
    def get_legal_moves_for_rook(self, row: int, col: int) -> list[tuple[int, int]]:
        return []

    def get_legal_moves_for_knight(self, row: int, col: int) -> list[tuple[int, int]]:
        legal_moves = []
        possible_moves = [
            (row+2, col+1),
            (row+2, col-1),
            (row-2, col+1),
            (row-2, col-1),
            (row+1, col+2),
            (row+1, col-2),
            (row-1, col+2),
            (row-1, col-2),
        ]
        for prow, pcol in possible_moves:
            if prow < 1 or prow > 8 or pcol < 1 or pcol > 8:
                continue
            if self.board.board[8-prow][pcol-1] != '.':
                occupying_piece = self.board.board[8-prow][pcol-1]
                logging.warning(f"Occupying piece: {occupying_piece} on turn {self.turn}")
                if self.turn == 'w' and occupying_piece.isupper():
                    continue
                if self.turn == 'b' and occupying_piece.islower():
                    continue
            legal_moves.append((prow, pcol))
        return legal_moves


    def get_legal_moves_for_bishop(self, row: int, col: int) -> list[tuple[int, int]]:
        return []


    def get_legal_moves_for_queen(self, row: int, col: int) -> list[tuple[int, int]]:
        return []


    def get_legal_moves_for_king(self, row: int, col: int) -> list[tuple[int, int]]:
        return []

        

        

if __name__ == "__main__":
    game = Game()
    print(game.board)
    piece_locations = game.get_piece_locations("w")
    possible_moves = []
    for location, piece in piece_locations:
        possible_moves += [{"start_loc": location, 
                            "end_loc": end_location,
                            "piece_type": piece}
                            for end_location in game.get_legal_moves(*location)]
    print(possible_moves)
    pass