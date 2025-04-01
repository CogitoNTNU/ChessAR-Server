from src.environment.positional import Chessboard, Corners, PiecePositions, Positional, PositionalParams
from src.   representation.representation import Representation
from typing import Any, List
from PIL import Image

from inference_sdk import InferenceHTTPClient


class WishBoneRepresentation(Representation):
    """Intakes a stream of images, using two YOLO models to capture chessboard state and outputs it"""

    def __init__(self, environment: Positional) -> None:
        self.environment = environment

    def YOLO_detect_corners(self, input: Any) -> List[Corners]:
        """YOLOV# model to detect corners of the chessboard"""
        pass


    def YOLO_detect_pieces(self, input: Any) -> List[PiecePositions]:
        """YOLOV# model to detect pieces and their positions"""
        image = Image.open("./src/representation/image.png")
        image = image.convert('RGB')

        CLIENT = InferenceHTTPClient(
            api_url="https://detect.roboflow.com",
            api_key="KWXDph0Kgrmgyro7XGtS"
        )

        board = CLIENT.infer(image, model_id="chess-piece-detection-5ipnt/3")
        
        

        return None

    def compute(self, input: Any) -> Chessboard:
        """
        Takes the input from the viewport and returns the state of the chess board.

        input - the stream or image input from the viewport.
        """
        bord_corners: List[Corners] = self.YOLO_detect_corners(input) # Get the corners of the chessboard

        pieces: List[PiecePositions] = self.YOLO_detect_pieces(input) # Get the pieces from the image

        chessboard = self.environment.to_env(PositionalParams(corner_positions=bord_corners, piece_positions=pieces))

        return chessboard

