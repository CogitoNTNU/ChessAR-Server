from src.viewport.viewport import ViewPort
from PIL import Image
from typing import Any, List
from src.environment.environment import Environment
from src.environment.positional import Positional, PiecePositions
from src.representation.representation import Representation
from src.representation.wishbone import WishBoneRepresentation
from src.environment.positional import Chessboard
import cv2


class MockViewport(ViewPort):
    """A mock viewport that returns a chessboard"""
    def __init__(self):
        environment: Environment = Positional()
        self.repr: Representation = WishBoneRepresentation(environment)
        

    # def get_output(self, image: Any) -> List[PiecePositions]:
    #     image = Image.open(image)
    #     image = image.convert('RGB')
        
    #     result = self.repr.YOLO_detect_pieces(image)

    #     return result
    
    def get_output(self) -> Chessboard:
        
        cap = cv2.VideoCapture(0)

        # Check if the camera opened successfully
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return []
        
        ret, frame = cap.read()
        cv2.imwrite("frame.jpg", frame)

        if ret:
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image = image.convert('RGB')
            

            result = self.repr.YOLO_detect_pieces(image)
        else:
            print("Error: Could not read frame.")
            return []

        cap.release()
        cv2.destroyAllWindows()
        
        return result