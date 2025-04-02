from dataclasses import dataclass

from classes.pieces import Piece


@dataclass
class Move:
    row: int
    col: int
    captured_piece: Piece | None
    piece: Piece
    in_check: bool
    has_moved: bool | None = None
