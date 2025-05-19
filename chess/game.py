import logging
from typing import Optional
from chess.board import Board
from chess.constants import POSITION
from chess.fen import STARTING_FEN_STR, Fen
from chess.exceptions import TurnOrderError
from chess.pieces import Empty, Piece


class Game:
    def __init__(self, fen: Optional[Fen] = Fen(STARTING_FEN_STR)):
        self.board = Board(fen)
        self.turn = fen.get_turn()
        self.current_player = 1 if self.turn == "w" else -1
        self.castles = fen.get_castles()
        self.en_passant = fen.get_en_passant()
        self.halfmove_clock = fen.get_halfmove_clock()
        self.fullmove_number = fen.get_fullmove_number()
        self.player_key = {"w":1, "b":-1}
        self.captured = {
            1: [],
            -1: []
        }

    def piece_matches_player(self, piece: Piece, player: Optional[int] = None) -> bool:
        if player is None:
            player = self.current_player

        return pos.piece.colour == player

    def get_piece_locations(self, player: int) -> list[POSITION]:
        locations = []
        for row in range(1, 9):
            for col in range(1, 9):
                pos = self.board.get_position(row, col)
                if self.piece_matches_player(pos, player):
                    locations.append(pos)

        return locations

    def get_legal_moves(self, pos: POSITION) -> list[POSITION]:
        piece = self.board._get_piece(*pos)
        logging.warning(f"Piece: {piece}")
        return piece.get_legal_moves(self.board, pos)
    
    def make_move(self, start_pos: POSITION, end_pos: POSITION):
    def make_move(self, start_pos: POSITION, end_pos: POSITION):
        if start_pos not in self.get_piece_locations(self.current_player):
            logging.warning(f"no valid piece in origin square {start_pos}")
            return
        
        legal_spaces = self.get_legal_moves(start_pos)
        if end_pos not in legal_spaces:
            logging.warning(f"the indicated piece cannot move to the indicated square")
            return
        
        start_piece = self.board._get_piece(*start_pos)
        end_piece = self.board._get_piece(*end_pos)
        
        if end_piece.piece_str != ".":
            self.captured[-1*self.current_player].append(end_piece)
        elif end_pos == self.en_passant and start_piece.piece_str.lower() == "p":
            self.captured[-1*self.current_player].append(self.board._get_piece(*self.en_passant))

        self.board.change_piece_in_location(*start_pos, Empty())
        self.board.change_piece_in_location(*end_pos, start_piece)
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