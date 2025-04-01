from src.viewport.viewport import ViewPort
from PIL import Image
from typing import Any, List
from src.environment.environment import Environment
from src.environment.positional import Positional, PiecePositions
from src.representation.representation import Representation
from src.representation.wishbone import WishBoneRepresentation
from src.environment.positional import Chessboard


class MockViewport(ViewPort):
    """A mock viewport that returns a chessboard"""
    def __init__(self):
        environment: Environment = Positional()
        self.repr: Representation = WishBoneRepresentation(environment)
        

    def get_output(self, image: Any) -> List[PiecePositions]:
        image = Image.open(image)
        image = image.convert('RGB')
        
        result = self.repr.YOLO_detect_pieces(image)

        return result
    