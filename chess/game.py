import logging
from copy import deepcopy
from typing import Optional

from chess.board import Board
from chess.constants import POSITION
from chess.fen import STARTING_FEN_STR, Fen
from chess.move import Move
from chess.pieces import Empty, King, Piece, Rook


class Game:
    def __init__(self, fen: Optional[Fen] = None):
        if fen is None:
            fen = Fen(STARTING_FEN_STR)
        self.board = Board(fen)
        self.turn = fen.get_turn()
        self.current_player = 1 if self.turn == "w" else -1
        self.castles = fen.get_castles()
        self.en_passant = fen.get_en_passant()
        self.halfmove_clock = fen.get_halfmove_clock()
        self.fullmove_number = fen.get_fullmove_number()
        self.player_key: dict[str, int] = {"w": 1, "b": -1}
        self.captured: dict[int, list[Piece]] = {1: [], -1: []}
        self.check_moves: list[Move] = []

    def check_if_in_check(
        self, player: Optional[int] = None, move: Optional[Move] = None
    ) -> bool:
        if not player:
            player = self.current_player
        checking_moves = []
        locations = self.get_piece_locations(-player)
        for location in locations:
            # TODO: Something funny happening here
            # Legal_moves is already a set of moves.
            # Feels like we're recalculating something
            legal_moves = self.get_legal_moves(*location, ignore_check=True)
            for legal_move in legal_moves:
                if self.board.get_piece(*legal_move.end_pos).name == "King":
                    checking_moves.append(
                        Move(
                            location,
                            legal_move.end_pos,
                            self.board.get_piece(*location),
                        )
                    )

        if len(checking_moves) > 0:
            return True
        else:
            return False

    def piece_matches_player(self, piece: Piece, player: Optional[int] = None) -> bool:
        if player is None:
            player = self.current_player

        logging.info(
            f"Checking piece {piece.piece_str} "
            f"(colour={piece.colour}) against player {player}"
        )
        return piece.colour == player

    def get_piece_locations(self, player: int) -> list[POSITION]:
        locations = []
        for row in range(1, 9):
            for col in range(1, 9):
                if self.piece_matches_player(self.board.get_piece(row, col), player):
                    locations.append((row, col))

        return locations

    def get_legal_moves(
        self, row: int, col: int, ignore_check: bool = False
    ) -> list[Move]:
        legal_moves: list[Move] = []
        piece = self.board.get_piece(row, col)
        match piece.name:
            case "Pawn":
                poss_legal_moves = self.get_legal_moves_pawn(row, col, piece.colour)
            case "Knight":
                poss_legal_moves = self.get_legal_moves_knight(row, col, piece.colour)
            case "Rook":
                poss_legal_moves = self.get_legal_moves_rook(row, col, piece.colour)
            case "Bishop":
                poss_legal_moves = self.get_legal_moves_bishop(row, col, piece.colour)
            case "Queen":
                poss_legal_moves = self.get_legal_moves_queen(row, col, piece.colour)
            case "King":
                poss_legal_moves = self.get_legal_moves_king(
                    row, col, piece.colour, ignore_check
                )
            case _:
                raise ValueError(f"Invalid piece: {piece.name}")

        if ignore_check:
            return poss_legal_moves
        else:
            print(f"Checking {len(poss_legal_moves)} moves")
            for move in poss_legal_moves:
                temp_game = deepcopy(self)
                temp_game.make_move(move)
                in_check = temp_game.check_if_in_check(piece.colour)
                if not in_check:
                    legal_moves.append(move)

            return legal_moves

    def get_legal_moves_knight(self, row: int, col: int, colour: int) -> list[Move]:
        legal_moves: list[Move] = []
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
            if piece.colour == colour:
                continue
            else:
                legal_moves.append(Move((row, col), square))
        return legal_moves

    def get_legal_moves_pawn(self, row: int, col: int, colour: int) -> list[Move]:
        legal_moves = []
        square_1 = (row + colour, col)
        square_2 = (row + 2 * colour, col)

        if (
            not self.board.is_impossible(*square_1)
            and self.board.get_piece(*square_1).piece_str == "."
        ):
            legal_moves.append(Move((row, col), square_1))
            if (
                not self.board.is_impossible(*square_2)
                and self.board.get_piece(*square_2).piece_str == "."
                and 2 * row == (9 - 5 * colour)
            ):
                legal_moves.append(Move((row, col), square_2))

        attack_squares = [
            (row + colour, col + 1),
            (row + colour, col - 1),
        ]
        for square in attack_squares:
            if not self.board.is_impossible(*square):
                if (
                    self.board.get_piece(*square).colour == -colour
                    or self.en_passant == square
                ):
                    legal_moves.append(Move((row, col), square))

        return legal_moves

    def get_legal_moves_rook(self, row: int, col: int, colour: int) -> list[Move]:
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
                if piece.colour == colour:
                    break
                elif piece.colour == -colour:
                    legal_moves.append(Move((row, col), square))
                    break
                else:
                    legal_moves.append(Move((row, col), square))

        return legal_moves

    def get_legal_moves_bishop(self, row: int, col: int, colour: int) -> list[Move]:
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
                if piece.colour == colour:
                    break
                elif piece.colour == -colour:
                    legal_moves.append(Move((row, col), square))
                    break
                else:
                    legal_moves.append(Move((row, col), square))

        return legal_moves

    def get_legal_moves_queen(self, row: int, col: int, colour: int) -> list[Move]:
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
                if piece.colour == colour:
                    break
                elif piece.colour == -colour:
                    legal_moves.append(Move((row, col), square))
                    break
                else:
                    legal_moves.append(Move((row, col), square))

        return legal_moves

    def get_legal_moves_king(
        self, row: int, col: int, colour: int, ignore_castle: bool = True
    ) -> list[Move]:
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
            if piece.colour == colour:
                continue
            elif piece.colour == -colour:
                legal_moves.append(Move((row, col), square))
                continue
            else:
                legal_moves.append(Move((row, col), square))

        # castling
        if not ignore_castle:
            if Piece(colour).matched_piece("k") in self.castles:
                safe_to_castle = True
                for empty_col in range(6, 8):
                    if self.board.get_piece(row, empty_col).name != "Empty":
                        safe_to_castle = False

                for king_col in range(5, 8):
                    temp_board = deepcopy(self)
                    temp_board.make_move(Move((row, col), (row, king_col)))
                    if temp_board.check_if_in_check(colour):
                        safe_to_castle = False

                if safe_to_castle:
                    legal_moves.append(
                        Move((row, col), (row, col + 2), piece=King(colour))
                    )

            if Piece(colour).matched_piece("q") in self.castles:
                safe_to_castle = True
                for empty_col in range(2, 5):
                    if self.board.get_piece(row, empty_col).name != "Empty":
                        safe_to_castle = False

                for king_col in range(3, 6):
                    temp_board = deepcopy(self)
                    temp_board.make_move(Move((row, col), (row, king_col)))
                    if temp_board.check_if_in_check(colour):
                        safe_to_castle = False

                if safe_to_castle:
                    legal_moves.append(
                        Move((row, col), (row, col - 2), piece=King(colour))
                    )

        return legal_moves

    def make_move(self, move: Move) -> None:
        start_pos = move.start_pos
        end_pos = move.end_pos
        if start_pos not in self.get_piece_locations(self.current_player):
            logging.warning(f"no valid piece in origin square {start_pos}")
            return

        print(start_pos, end_pos)
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

        if start_piece.name == "King":
            self.castles = [
                i for i in self.castles if i != start_piece.matched_piece("k")
            ]
            self.castles = [
                i for i in self.castles if i != start_piece.matched_piece("q")
            ]

        if start_piece.name == "Rook":
            if start_pos[1] == 1:
                self.castles = [
                    i for i in self.castles if i != start_piece.matched_piece("q")
                ]
            elif start_pos[1] == 8:
                self.castles = [
                    i for i in self.castles if i != start_piece.matched_piece("k")
                ]

        if start_piece.name == "King" and abs(start_pos[1] - end_pos[1]) == 2:
            if end_pos[1] < start_pos[1]:
                self.board.change_piece_in_location(start_pos[0], 1, Empty())
                self.board.change_piece_in_location(
                    start_pos[0], 4, Rook(start_piece.colour)
                )
            elif end_pos[1] > start_pos[1]:
                self.board.change_piece_in_location(start_pos[0], 8, Empty())
                self.board.change_piece_in_location(
                    start_pos[0], 6, Rook(start_piece.colour)
                )

        self.board.change_piece_in_location(*start_pos, Empty())
        self.board.change_piece_in_location(*end_pos, start_piece)
        print(self.board)

        self.current_player *= -1


if __name__ == "__main__":
    game = Game()
    print(game.board)
    piece_locations = game.get_piece_locations(game.current_player)
    possible_moves = [
        Move(start_pos=piece_location, end_pos=end_location.end_pos)
        for piece_location in game.get_piece_locations(game.current_player)
        for end_location in game.get_legal_moves(*piece_location)
    ]
    print(possible_moves)
    print(possible_moves[0])
    game.make_move(possible_moves[0])
    print(game.board)
    pass
