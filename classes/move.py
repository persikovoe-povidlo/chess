from dataclasses import dataclass

from classes.pieces import Piece


@dataclass
class Move:
    row1: int
    col1: int
    row2: int
    col2: int
    captured_piece: Piece | None
    piece: Piece
