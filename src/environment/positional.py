from typing import List

from src.environment.environment import Environment
import numpy as np
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

class BoardSpacePiece(BaseModel):
    vec: np.ndarray
    piece: Piece



class Positional(Environment):
    """Implements an environment that intakes positional arguments from an image, the corner positions and all the piece positions detected"""
    def is_valid(self, state: Chessboard) -> bool:
        """
        Checks if the fens string is a valid chessboard state

        Args:
            state (Chessboard): The chessboard string to validate

        Returns:
            bool: True if the state is a valid chessboard state, False otherwise
        """
        env = Fen()
        return env.is_valid(fen)
    

    def find_transformation_matrix(corners: List[Corners]) -> np.ndarray:
        """
        Finds the transformation vector to convert from screen space to board space given the corners of the chess board
        Args:
            corners (List[Corners]): List of corners of chess board in screen space
        Returns:
            np.ndarray: 2D transformation matrix 
        """
        start_point = corners[0]
        vecs = []
        for point in corners:
            if point == start_point: continue
            vecs.append(np.array([point.x-start_point.x, point.y-start_point.y]))

        lowest_dot = 100000
        index_ldot = []
        for i in range(len(vecs)):
            for j in range(j, len(vecs)):
                dot = np.abs(np.linalg.vecdot(np.linalg.norm(vecs[i]), np.linalg.norm(vecs[j])))
                if dot < lowest_dot:
                    lowest_dot = dot
                    index_ldot = [i, j]
        vec1 = vecs[index_ldot[0]]
        vec2 = vecs[index_ldot[1]]

        n_vec_1 = np.array([1,0])
        n_vec_2 = np.array([0,1])

        matrix = np.linalg.matmul(np.array([n_vec_1, n_vec_2]), np.linalg.inv([vec1, vec2]))

        return matrix

    def transform_to_board_vector(transform_matrix: np.ndarray, vec: np.ndarray) -> np.ndarray:
        """
        Transform a piece position from screen space to board space using the transformation matrix
        Args:
            transformation_matrix (np.ndarray): 2d transformation matrix
            vec (np.ndarray): 2d vector in screen space to transform to board space
        Returns:
            np.ndarray: 2d vector in board space
        """
        return np.linalg.matmul(transform_matrix, vec)

    def get_piece_positions_in_board_space(self, board: PositionalParams) -> List[BoardSpacePiece]:
        """
        Takes in a board in screen space, and transform all pieces position to a vector relative to corners[0]
        Args:
            board (PositionalParams): A chess board where positions are in screen space
        Returns:
            List[BoardSpacePiece]: List of all pieces with positions given with a vector relative to corners[0]
        """
        corners = board.corner_positions
        pieces = board.piece_positions

        t_matrix = self.find_transformation_matrix(corners)

        board_space_piece_pos = []

        for piece in pieces:
            vec = np.array([piece.x - corners[0].x, piece.y - corners[0].y])
            board_space = BoardSpacePiece(self.transform_to_board_vector(t_matrix, vec), piece.piece)
            board_space_piece_pos.append(board_space)
        
        return board_space_piece_pos
    
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
        for piece in pieces:
            row = round(piece.vec.x * 8)
            col = round(piece.vec.y * 8)
            if chessboard[row][col] == "":
                chessboard[row][col] = piece.piece
            else:
                print(f"Error: pieces {piece.piece} and {chessboard[row][col]} have the same position!")
        
        return chessboard


    def find_transformation_matrix(corners: List[Corners]) -> np.ndarray:
        """
        Finds the transformation vector to convert from screen space to board space given the corners of the chess board
        Args:
            corners (List[Corners]): List of corners of chess board in screen space
        Returns:
            np.ndarray: 2D transformation matrix 
        """
        start_point = corners[0]
        vecs = []
        for point in corners:
            if point == start_point: continue
            vecs.append(np.array([point.x-start_point.x, point.y-start_point.y]))

        lowest_dot = 100000
        index_ldot = []
        for i in range(len(vecs)):
            for j in range(j, len(vecs)):
                dot = np.abs(np.linalg.vecdot(np.linalg.norm(vecs[i]), np.linalg.norm(vecs[j])))
                if dot < lowest_dot:
                    lowest_dot = dot
                    index_ldot = [i, j]
        vec1 = vecs[index_ldot[0]]
        vec2 = vecs[index_ldot[1]]

        n_vec_1 = np.array([1,0])
        n_vec_2 = np.array([0,1])

        matrix = np.linalg.matmul(np.array([n_vec_1, n_vec_2]), np.linalg.inv([vec1, vec2]))

        return matrix

    def transform_to_board_vector(transform_matrix: np.ndarray, vec: np.ndarray) -> np.ndarray:
        """
        Transform a piece position from screen space to board space using the transformation matrix
        Args:
            transformation_matrix (np.ndarray): 2d transformation matrix
            vec (np.ndarray): 2d vector in screen space to transform to board space
        Returns:
            np.ndarray: 2d vector in board space
        """
        return np.linalg.matmul(transform_matrix, vec)

    def get_piece_positions_in_board_space(self, board: PositionalParams) -> List[BoardSpacePiece]:
        """
        Takes in a board in screen space, and transform all pieces position to a vector relative to corners[0]
        Args:
            board (PositionalParams): A chess board where positions are in screen space
        Returns:
            List[BoardSpacePiece]: List of all pieces with positions given with a vector relative to corners[0]
        """
        corners = board.corner_positions
        pieces = board.piece_positions

        t_matrix = self.find_transformation_matrix(corners)

        board_space_piece_pos = []

        for piece in pieces:
            vec = np.array([piece.x - corners[0].x, piece.y - corners[0].y])
            board_space = BoardSpacePiece(self.transform_to_board_vector(t_matrix, vec), piece.piece)
            board_space_piece_pos.append(board_space)
        
        return board_space_piece_pos
    
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
        for piece in pieces:
            row = round(piece.vec.x * 8)
            col = round(piece.vec.y * 8)
            if chessboard[row][col] == "":
                chessboard[row][col] = piece.piece
            else:
                print(f"Error: pieces {piece.piece} and {chessboard[row][col]} have the same position!")
        
        return chessboard


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