from abc import ABC, abstractmethod
from typing import Any

"""
This implements a standard viewport interface to be used as a base for all viewports.
"""

class ViewPort(ABC):
    """
    This interface defines how all viewport layer should work.

    The viewport layer is responsible for retrieving an human observable state of a chess game, IE. an image of a chess board or a video.
    This can be implmented in any way, there is an example using images and OpenCV module.

    The viewport layer must implement the following methods:
    - `get_output()`: Returns the current state of the chess board as a stream or image.

    """

    @abstractmethod
    def get_output(self) -> Any:
        """
        Returns the current state of the chess board as a stream or image.
        """
        pass
