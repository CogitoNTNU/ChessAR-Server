from typing import List

from src.environment.environment import Environment

from pydantic import BaseModel

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


class Positional(Environment):
    """Implements an environment that intakes positional arguments from an image, the corner positions and all the piece positions detected"""

    def to_env(self, repr_state: PositionalParams) -> Chessboard:
        """
        Converts/maps the repr_state (positional arguments) to a 2D array of pieces.

        Args:
            repr_state: The provided positional information

        Returns:
            Chessboard: The environment state, a chess board
        """
        pass

    def is_valid(self, state: Chessboard) -> bool:
        """
        Checks if the fens string is a valid chessboard state

        Args:
            state (Chessboard): The chessboard string to validate

        Returns:
            bool: True if the state is a valid chessboard state, False otherwise
        """
        pass

    def to_fen(self, state: Chessboard) -> fen:
        pass
