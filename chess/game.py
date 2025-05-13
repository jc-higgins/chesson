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
        self.player_key = {"w":1, "b":-1}
        self.current_player = 1
        self.captured = {
            1: [],
            -1: []
        }

    def get_piece_locations(self, player: int):
        locations = []
        if player in ["w", "b"]:
            player = self.player_key[player]

        if player == 1:
            matches_upper = True
        elif player == -1:
            matches_upper = False
        else:
            logging.warning("player format is not valid. use value in (-1, 1)")
            return []
        
        for row in range(1, 9):
            for col in range(1, 9):
                piece = self.board.get_piece_in_location(row, col)
                if (piece == piece.upper()) == matches_upper and piece != '.':
                    locations.append(((row, col), piece))

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
    
    def make_move(self, start_loc: tuple[int], end_loc: tuple[int]):
        
        piece = self.board.get_piece_in_location(*start_loc)

        if (start_loc, piece) not in self.get_piece_locations(self.current_player):
            logging.warning(f"no valid piece in origin square {start_loc}")
            return
        
        legal_spaces = self.get_legal_moves(*start_loc)
        if end_loc not in legal_spaces:
            logging.warning(f"the indicated piece cannot move to the indicated square")
            return
        
        
        if self.board.get_piece_in_location(*end_loc) != ".":
            self.captured[-1*self.current_player].append(self.board.get_piece_in_location(*end_loc))
        self.board.change_piece_in_location(*end_loc, piece)
        self.board.change_piece_in_location(*start_loc, ".")

        self.current_player *= -1
        
        


if __name__ == "__main__":
    game = Game()
    print(game.board)
    piece_locations = game.get_piece_locations(game.current_player)
    possible_moves = []
    for location, piece in piece_locations:
        possible_moves += [{"start_loc": location, 
                            "end_loc": end_location}
                            for end_location in game.get_legal_moves(*location)]
    print(possible_moves)

    game.make_move(**possible_moves[0])
    print(game.board)
    pass