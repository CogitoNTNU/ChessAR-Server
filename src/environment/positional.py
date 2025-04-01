from typing import List

from src.environment.environment import Environment
from src.environment.fen import Fen

from pydantic import BaseModel
import chess

# This is a type alias for a fen string
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
    """The positional arguments for the environment"""
    corner_positions: List[Corners]
    piece_positions: List[PiecePositions]

class SquarePosition(BaseModel):
    x: float
    y: float


class Positional(Environment):
    """Implements an environment that intakes positional arguments from an image, the corner positions and all the piece positions detected"""
    def __init__(self):
        self.state = [[Piece() for _ in range(8)] for __ in range(8)]
        self.square_positions = []

    def get_square_positions(corners: List[Corners]) -> SquarePosition:
        pass

    def closest_chess_square(square_pos: List[SquarePosition], piece: PiecePositions) -> int:
        pass

    def to_env(self, repr_state: PositionalParams) -> Chessboard:
        """
        Converts/maps the repr_state (positional arguments) to a 2D array of pieces.

        Args:
            repr_state: The provided positional information

        Returns:
            Chessboard: The environment state, a chess board
        """
        pass


    def is_valid(self, fen: fen) -> bool:
        """
        Checks if the fens string is a valid chessboard state

        Args:
            state (Chessboard): The chessboard string to validate

        Returns:
            bool: True if the state is a valid chessboard state, False otherwise
        """
        env = Fen()
        return env.is_valid(fen)

    def to_fen(self, state: Chessboard) -> fen:
        fen = ""
        num = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != "":
                    if num > 0:
                        fen += str(num)
                        num = 0
                    fen += state[i][j]
                else:
                    num += 1
            if num > 0:
                fen += str(num)
                num = 0
            if i < len(state)-1:
                fen += "/"
        fen += " w - - 0 0"
        return fen