import logging
from typing import Optional
from chess.board import Board
from chess.fen import STARTING_FEN_STR, Fen
from chess.exceptions import TurnOrderError
from chess.position import Position


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

    def make_move(self, start: Position, end: Position):
        ...

    def get_legal_moves(self, pos: Position) -> list[Position]:
        logging.warning(f"Piece: {pos.piece}")
        piece = pos.piece.lower()
        match piece:
            case 'p':
                return self.get_legal_moves_for_pawn(pos)
            case 'r':
                return self.get_legal_moves_for_rook(pos)
            case 'n':
                return self.get_legal_moves_for_knight(pos)
            case 'b':
                return self.get_legal_moves_for_bishop(pos)
            case 'q':
                return self.get_legal_moves_for_queen(pos)
            case 'k':
                return self.get_legal_moves_for_king(pos)
            case '.':
                return []
            case _:
                logging.warning(f"No matching case for piece: {piece}")
                return []
            

    def get_legal_moves_for_pawn(self, position: Position) -> list[Position]:
        legal_moves: list[Position] = []
        possible_moves: list[Position] = []
        row, col = position.row, position.col
        if self.turn == 'w':
            if row == 2:
                possible_moves.append(self.board.get_position(row+2, col))
            possible_moves.append(self.board.get_position(row+1, col))
        else:
            if row == 7:
                possible_moves.append(self.board.get_position(row-2, col))
            possible_moves.append(self.board.get_position(row-1, col))
        
        # TODO: Add diagonal takes
        # TODO: Add en passant
        # TODO: Add promotion

        for move in possible_moves:
            if move.is_impossible():
                continue
            if move.piece != '.':
                continue
            legal_moves.append(move)
        return legal_moves
        
    def get_legal_moves_for_rook(self, pos: Position) -> list[Position]:
        return []

    def get_legal_moves_for_knight(self, pos: Position) -> list[Position]:
        row, col = pos.row, pos.col
        legal_moves: list[Position] = []
        possible_moves = [
            self.board.get_position(row+2, col+1),
            self.board.get_position(row+2, col-1),
            self.board.get_position(row-2, col+1),
            self.board.get_position(row-2, col-1),
            self.board.get_position(row+1, col+2),
            self.board.get_position(row+1, col-2),
            self.board.get_position(row-1, col+2),
            self.board.get_position(row-1, col-2),
        ]
        for pos_move in possible_moves:
            if pos_move.is_impossible():
                continue
            if pos_move.piece != '.':
                logging.warning(f"Occupying piece: {pos_move.piece} on turn {self.turn}")
                if self.turn == 'w' and pos_move.piece.isupper():
                    continue
                if self.turn == 'b' and pos_move.piece.islower():
                    continue
            legal_moves.append(pos_move)
        return legal_moves


    def get_legal_moves_for_bishop(self, pos: Position) -> list[Position]:
        return []


    def get_legal_moves_for_queen(self, pos: Position) -> list[Position]:
        return []


    def get_legal_moves_for_king(self, pos: Position) -> list[Position]:
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