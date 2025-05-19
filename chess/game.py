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
        self.current_player = 1 if self.turn == "w" else -1
        self.castles = fen.get_castles()
        self.en_passant = fen.get_en_passant()
        self.halfmove_clock = fen.get_halfmove_clock()
        self.fullmove_number = fen.get_fullmove_number()
        self.player_key = {"w": 1, "b": -1}
        self.captured = {1: [], -1: []}

    def piece_matches_player(self, piece: Piece, player: Optional[int] = None) -> bool:
        if player is None:
            player = self.current_player

        logging.info(
            f"Checking piece {piece.piece_str} (colour={piece.colour}) against player {player}"
        )
        return piece.colour == player

    def get_piece_locations(self, player: int) -> list[POSITION]:
        locations = []
        for row in range(1, 9):
            for col in range(1, 9):
                if self.piece_matches_player(self.board.get_piece(row, col), player):
                    locations.append((row, col))

        return locations

    def get_legal_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        match piece.name:
            case "Pawn":
                return self.get_legal_moves_pawn(row, col)
            case "Knight":
                return self.get_legal_moves_knight(row, col)
            case "Rook":
                return self.get_legal_moves_rook(row, col)
            case "Bishop":
                return self.get_legal_moves_bishop(row, col)
            case "Queen":
                return self.get_legal_moves_queen(row, col)
            case "King":
                return self.get_legal_moves_king(row, col)

    def get_legal_moves_knight(self, row: int, col: int):
        legal_moves: list[POSITION] = []
        possible_moves = [
            (row + 2, col + 1),
            (row + 2, col - 1),
            (row - 2, col + 1),
            (row - 2, col - 1),
            (row + 1, col + 2),
            (row + 1, col - 2),
            (row - 1, col + 2),
            (row - 1, col - 2),
        ]

        for square in possible_moves:
            if self.board.is_impossible(*square):
                continue
            piece = self.board.get_piece(*square)
            if piece.colour == self.current_player:
                continue
            else:
                legal_moves.append(square)
        return legal_moves

    def get_legal_moves_pawn(self, row: int, col: int):
        legal_moves = []
        square_1 = (row + self.current_player, col)
        square_2 = (row + 2 * self.current_player, col)

        if (
            not self.board.is_impossible(*square_1)
            and self.board.get_piece(*square_1).piece_str == "."
        ):
            legal_moves.append(square_1)
            if (
                not self.board.is_impossible(*square_2)
                and self.board.get_piece(*square_2).piece_str == "."
                and 2 * row == (9 - 5 * self.current_player)
            ):
                legal_moves.append(square_2)

        attack_squares = [
            (row + self.current_player, col + 1),
            (row + self.current_player, col - 1),
        ]
        for square in attack_squares:
            if not self.board.is_impossible(*square):
                if (
                    self.board.get_piece(*square).colour == -self.current_player
                    or self.en_passant == square
                ):
                    legal_moves.append(square)

        return legal_moves

    def get_legal_moves_rook(self, row: int, col: int):
        legal_moves = []

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = (row + steps * dir[0], col + steps * dir[1])
                if self.board.is_impossible(*square):
                    break
                piece = self.board.get_piece(*square)
                if piece.colour == self.current_player:
                    break
                elif piece.colour == -self.current_player:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves

    def get_legal_moves_bishop(self, row: int, col: int):
        legal_moves = []

        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = (row + steps * dir[0], col + steps * dir[1])
                if self.board.is_impossible(*square):
                    break
                piece = self.board.get_piece(*square)
                if piece.colour == self.current_player:
                    break
                elif piece.colour == -self.current_player:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves

    def get_legal_moves_queen(self, row: int, col: int):
        legal_moves = []

        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for dir in directions:
            steps = 0
            while True:
                steps += 1
                square = (row + steps * dir[0], col + steps * dir[1])
                if self.board.is_impossible(*square):
                    break
                piece = self.board.get_piece(*square)
                if piece.colour == self.current_player:
                    break
                elif piece.colour == -self.current_player:
                    legal_moves.append(square)
                    break
                else:
                    legal_moves.append(square)

        return legal_moves

    def get_legal_moves_king(self, row: int, col: int):
        legal_moves = []

        directions = [
            (0, 1),
            (0, -1),
            (1, 0),
            (-1, 0),
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
        ]

        for dir in directions:
            square = (row + dir[0], col + dir[1])
            if self.board.is_impossible(*square):
                continue
            piece = self.board.get_piece(*square)
            if piece.colour == self.current_player:
                continue
            elif piece.colour == -self.current_player:
                legal_moves.append(square)
                continue
            else:
                legal_moves.append(square)

        return legal_moves

    def make_move(self, start_pos: POSITION, end_pos: POSITION):
        if start_pos not in self.get_piece_locations(self.current_player):
            logging.warning(f"no valid piece in origin square {start_pos}")
            return

        legal_spaces = self.get_legal_moves(*start_pos)
        if end_pos not in legal_spaces:
            logging.warning(f"the indicated piece cannot move to the indicated square")
            return

        start_piece = self.board.get_piece(*start_pos)
        end_piece = self.board.get_piece(*end_pos)

        if end_piece.piece_str != ".":
            self.captured[-1 * self.current_player].append(end_piece)
        elif end_pos == self.en_passant and start_piece.name == "Pawn":
            self.captured[-1 * self.current_player].append(
                self.board.get_piece(end_pos[0] - self.current_player, end_pos[1])
            )
            self.board.change_piece_in_location(
                end_pos[0] - self.current_player, end_pos[1], Empty()
            )

        if start_piece.name == "Pawn" and abs(start_pos[0] - end_pos[0]) == 2:
            self.en_passant = ((start_pos[0] + end_pos[0]) // 2, start_pos[1])
        else:
            self.en_passant = (-1, -1)

        self.board.change_piece_in_location(*start_pos, Empty())
        self.board.change_piece_in_location(*end_pos, start_piece)
        print(self.board)

        self.current_player *= -1


if __name__ == "__main__":
    game = Game()
    print(game.board)
    piece_locations = game.get_piece_locations(game.current_player)
    possible_moves = []
    for piece_location in piece_locations:
        possible_moves += [
            {"start_pos": piece_location, "end_pos": end_location}
            for end_location in game.get_legal_moves(*piece_location)
        ]

    print(possible_moves[0])
    game.make_move(**possible_moves[0])
    print(game.board)
    pass
