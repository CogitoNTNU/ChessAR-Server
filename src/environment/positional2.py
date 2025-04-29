# src/environment/positional_env.py
from typing import List, Tuple, Literal
import numpy as np
import cv2
from pydantic import BaseModel
from src.environment.environment import Environment
from src.environment.fen import Fen

fen = str
Piece = str
Chessboard = List[List[Piece]]

class Corners(BaseModel):
    x: float
    y: float
    width: float
    height: float

class PiecePositions(BaseModel):
    x: float
    y: float
    piece: Piece
    probability: float

class PositionalParams(BaseModel):
    corner_positions: List[Corners]
    piece_positions: List[PiecePositions]


def order_corners(corners: List[Corners]) -> np.ndarray:
    """
    Order four detected corners consistently as topleftl, topright, bottomright, bottomleft
    """
    pts = np.array([[c.x, c.y] for c in corners], dtype="float32")
    # sort by y-coordinate
    idx = np.argsort(pts[:, 1])
    top = pts[idx[:2]]
    bottom = pts[idx[2:]]
    tl, tr = sorted(top, key=lambda p: p[0])
    bl, br = sorted(bottom, key=lambda p: p[0])
    return np.array([tl, tr, br, bl], dtype="float32")


def get_perspective_transform(ordered: np.ndarray, board_size: int = 800) -> np.ndarray:
    """
    Compute the perspective transform matrix to warp to a square of size board_size
    """
    dst = np.array([
        [0, 0],
        [board_size - 1, 0],
        [board_size - 1, board_size - 1],
        [0, board_size - 1]
    ], dtype="float32")
    return cv2.getPerspectiveTransform(ordered, dst)


def warp_point(pt: Tuple[float, float], M: np.ndarray) -> Tuple[float, float]:
    """
    Apply perspective transform to a single point
    """
    src = np.array([[[pt[0], pt[1]]]], dtype="float32")
    dst = cv2.perspectiveTransform(src, M)[0][0]
    return float(dst[0]), float(dst[1])

class Positional(Environment):
    type: Literal["positional_environment"] = "positional_environment"

    def to_env(self, repr_state: PositionalParams) -> Chessboard:
        ordered = order_corners(repr_state.corner_positions)
        M = get_perspective_transform(ordered)
        board_size = 800
        square = board_size / 8.0

        board: Chessboard = [["" for _ in range(8)] for _ in range(8)]
        for p in sorted(repr_state.piece_positions, key=lambda pp: pp.probability, reverse=True):
            x_w, y_w = warp_point((p.x, p.y), M)
            col = int(x_w // square)
            row = int(y_w // square)
            col = max(0, min(7, col))
            row = max(0, min(7, row))
            board[row][col] = p.piece
        return board

    def to_fen(self, state: Chessboard) -> fen:
        fen_str = ""
        for i, row in enumerate(state):
            empty = 0
            for cell in row:
                if cell == "":
                    empty += 1
                else:
                    if empty:
                        fen_str += str(empty)
                        empty = 0
                    fen_str += cell
            if empty:
                fen_str += str(empty)
            if i < len(state) - 1:
                fen_str += "/"
        fen_str += " w - - 0 0"
        return fen_str

    def is_valid(self, state: Chessboard) -> bool:
        env = Fen()
        return env.is_valid(self.to_fen(state))


