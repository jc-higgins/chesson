STARTING_FEN_STR = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Fen:
    def __init__(self, fen: str = STARTING_FEN_STR):
        self.fen_str = fen

    def get_board_str(self) -> str:
        return self.fen_str.split()[0]

    def get_turn(self) -> str:
        return self.fen_str.split()[1]

    def get_castles(self) -> list[str]:
        return list(self.fen_str.split()[2])

    def get_en_passant(self) -> tuple[int, int]:
        en_passant_str = self.fen_str.split()[3]
        if en_passant_str == "-":
            return (-1, -1)
        else:
            return (int(en_passant_str[1]), ord(en_passant_str[0]) - 96)

    def get_halfmove_clock(self) -> str:
        return self.fen_str.split()[4]

    def get_fullmove_number(self) -> str:
        return self.fen_str.split()[5]
