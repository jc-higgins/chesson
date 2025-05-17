import logging
from typing import Optional
from chess.board import Board
from chess.fen import STARTING_FEN_STR, Fen
from chess.exceptions import TurnOrderError
from chess.position import Position
from chess.pieces import Empty


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

    def piece_matches_player(self, pos: Position, player: Optional[int] = None) -> bool:
        if player is None:
            player = self.current_player

        return pos.piece.colour == player

    def get_piece_locations(self, player: int) -> list[Position]:
        locations = []
        for row in range(1, 9):
            for col in range(1, 9):
                pos = self.board.get_position(row, col)
                if self.piece_matches_player(pos, player):
                    locations.append(pos)

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
    
    def make_move(self, start_pos: Position, end_pos: Position):
        if start_pos not in self.get_piece_locations(self.current_player):
            logging.warning(f"no valid piece in origin square {start_pos}")
            return
        
        legal_spaces = start_pos.piece.get_legal_moves(self.board, start_pos)
        if end_pos not in legal_spaces:
            logging.warning(f"the indicated piece cannot move to the indicated square")
            return
        
        if end_pos.piece.piece_str != ".":
            self.captured[-1*self.current_player].append(end_pos.piece)

        
        abandoned_pos = Position(start_pos.row, start_pos.col, Empty())
        entered_pos = Position(end_pos.row, end_pos.col, start_pos.piece)
        print("end_pos", end_pos.row, end_pos.col, end_pos.piece)
        self.board.change_piece_in_location(abandoned_pos)
        self.board.change_piece_in_location(entered_pos)
        print(self.board)

        self.current_player *= -1
        
        


if __name__ == "__main__":
    game = Game()
    print(game.board)
    piece_locations = game.get_piece_locations(game.current_player)
    print([(i.row, i.col, i.piece.piece_str) for i in piece_locations])
    possible_moves = []
    for piece_location in piece_locations:
        possible_moves += [{"start_pos": piece_location, 
                            "end_pos": end_location}
                            for end_location in piece_location.piece.get_legal_moves(game.board, piece_location)]

    print(possible_moves[0])
    game.make_move(**possible_moves[0])
    print(game.board)
    pass