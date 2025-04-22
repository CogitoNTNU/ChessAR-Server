from typing import Literal
from PIL import Image
from src.viewport.viewport import ViewPort

ViewPortImage = Image.Image

PATH_IMAGES = "./misc/images/"

class SnapShot(ViewPort):
    type: Literal["snapshot_viewport"] = "snapshot_viewport"

    def get_output(self) -> ViewPortImage:
        """
        Returns a random image of a chess board or a specified one.
        """

        return Image.open(f"{PATH_IMAGES}chessboard.jpg")
