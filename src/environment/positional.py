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
    corner_positions: List[Corners] | None
    piece_positions: List[PiecePositions] | None

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
        fen = ""
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
                fen += "num"
                num = 0
            fen += "/"

        return fen