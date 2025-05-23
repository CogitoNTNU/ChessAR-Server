from typing import List, Literal

from src.environment.environment import Environment
import numpy as np
from src.environment.fen import Fen

from pydantic import BaseModel

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

def piece_to_fen(piece: str) -> str:
    """
    Map a piece string to the correct FEN letter.
    Assumes format like 'white-pawn', 'black-knight', etc.
    """
    mapping = {
        "pawn": "p",
        "knight": "n",
        "bishop": "b",
        "rook": "k",
        "queen": "q",
        "king": "k"
    }

    try:
        color, kind = piece.lower().split("-")
        if kind not in mapping:
            raise ValueError(f"Unknown piece kind: {kind}")
        symbol = mapping[kind]
        return symbol.upper() if color == "white" else symbol
    except Exception as e:
        raise ValueError(f"Invalid piece format '{piece}': {e}")

class Positional(Environment):
    type: Literal["positional_environment"] = "positional_environment"

    """Implements an environment that intakes positional arguments from an image, the corner positions and all the piece positions detected"""

    def to_env(self, repr_state: PositionalParams) -> Chessboard:
        """
        Transforms all piece positions from screen space to board space. Then snap them to the nearest square.

        Args:
            repr_state (PositionalParams): A representation of a chess board where positions are in screen space

        Returns:
            Chessboard: 2d matrix representation of the chessboard
        """
        chessboard = [["" for _ in range(8)] for __ in range(8)]
        pieces = self.get_piece_positions_in_board_space(repr_state)
        if pieces is None:
            return None
        
        for piece in pieces:
            row = int(piece.x * 8)
            col = int(piece.y * 8)
            try:
                if chessboard[row][col] == "":
                    chessboard[row][col] = piece.piece
                else:
                    print(f"Error: pieces {piece.piece} and {chessboard[row][col]} are on the same square!")
            except:
                print("Pieces not placed correctly")
                return None
        return chessboard

    def find_transformation_matrix(self, corners: List[Corners]) -> np.ndarray:
        """
        Finds the transformation vector to convert from screen space to board space given the corners of the chess board
        Args:
            corners (List[Corners]): List of corners of chess board in screen space
        Returns:
            np.ndarray: 2D transformation matrix
        """
        try:
            start_point = corners[0]
            vecs = []
            for point in corners:
                if point == start_point: continue
                vecs.append(np.array([point.x-start_point.x, point.y-start_point.y]))
        except:
            print(f"Could not find corners.")
            return None


        lowest_dot = 100000
        index_ldot = []
        for i in range(len(vecs)):
            for j in range(i, len(vecs)):
                dot = np.abs(np.dot(vecs[i] / np.linalg.norm(vecs[i]), vecs[j] / np.linalg.norm(vecs[j])))
                if dot < lowest_dot:
                    lowest_dot = dot
                    index_ldot = [i, j]
        vec1 = vecs[index_ldot[0]]
        vec2 = vecs[index_ldot[1]]

        n_vec_1 = np.array([1,0])
        n_vec_2 = np.array([0,1])

        matrix = np.matmul(np.array([n_vec_1, n_vec_2]), np.linalg.inv(np.array([vec1, vec2])))

        return matrix

    def transform_to_board_space_vector(self, transform_matrix: np.ndarray, vec: np.ndarray) -> np.ndarray:
        """
        Transform a piece position from screen space to board space using the transformation matrix
        Args:
            transformation_matrix (np.ndarray): 2d transformation matrix
            vec (np.ndarray): 2d vector in screen space to transform to board space
        Returns:
            np.ndarray: 2d vector in board space
        """
        return np.matmul(transform_matrix, vec)

    def get_piece_positions_in_board_space(self, board: PositionalParams) -> List[PiecePositions]:
        """
        Takes in a board in screen space, and transform all pieces position to a vector relative to corners[0]
        Args:
            board (PositionalParams): A chess board where positions are in screen space
        Returns:
            List[PiecePositions]: List of all pieces with positions given with a vector relative to corners[0]
        """
        corners = board.corner_positions
        pieces = board.piece_positions

        t_matrix = self.find_transformation_matrix(corners)
        if t_matrix is None:
            return None

        board_space_piece_pos = []

        for piece in pieces:
            vec = np.array([piece.x - corners[0].x, piece.y - corners[0].y])
            transformation = self.transform_to_board_space_vector(t_matrix, vec)
            board_space = PiecePositions(x=transformation[0], y=transformation[1], piece=piece.piece, probability=piece.probability)
            board_space_piece_pos.append(board_space)

        return board_space_piece_pos


    def is_valid(self, state: Chessboard) -> bool:
        """
        Checks if the fens string is a valid chessboard state

        Args:
            state (Chessboard): The chessboard string to validate

        Returns:
            bool: True if the state is a valid chessboard state, False otherwise
        """
        env = Fen()
        return env.is_valid(self.to_fen(state))


    def to_fen(self, state: Chessboard) -> fen:
        fen = ""
        num = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != "":
                    if num > 0:
                        fen += str(num)
                        num = 0
                    fen += piece_to_fen(state[i][j])
                else:
                    num += 1
            if num > 0:
                fen += str(num)
                num = 0
            if i < len(state)-1:
                fen += "/"
        fen += " w - - 1 2"
        return fen
