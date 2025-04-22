from src.environment.positional import Chessboard, Corners, PiecePositions, Positional, PositionalParams
from src.representation.representation import Representation
from typing import List, Literal
from PIL import Image
from src.viewport.snapshot import ViewPortImage


class WishBone(Representation):
    type: Literal["wishbone_environment"] = "wishbone_environment"

    """Intakes an image, using two YOLO models to capture chessboard state and outputs it"""

    def __init__(self, environment: Positional) -> None:
        self.environment = environment

    def YOLO_detect_corners(self, input: ViewPortImage) -> List[Corners]:
        """YOLOV# model to detect corners of the chessboard"""
        pass


    def YOLO_detect_pieces(self, input: ViewPortImage) -> List[PiecePositions]:
        """YOLOV# model to detect pieces and their positions"""
        pass

    def compute(self, input: Image.Image) -> Chessboard:
        """
        Takes the input from the viewport and returns the state of the chess board.

        input - the stream or image input from the viewport.
        """
        bord_corners: List[Corners] = self.YOLO_detect_corners(input) # Get the corners of the chessboard

        pieces: List[PiecePositions] = self.YOLO_detect_pieces(input) # Get the pieces from the image

        positional_params = PositionalParams(corner_positions=bord_corners, piece_positions=pieces)

        chessboard = self.environment.to_env(positional_params)

        return chessboard
