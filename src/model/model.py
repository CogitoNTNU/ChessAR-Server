from abc import ABC, abstractmethod
from typing import Any

"""
This interface is responsible for defining the chess model at use to get the best possible moves.
"""


class Model(ABC):
    """
    This interface defines how we retrieve the best possible chess move from a given state on the chess board.

    The model layer is responsible for taking the current state of the chess board and returning the best possible move.

    The model layer must implement the following methods:
    - `get_best_move()`: Returns the best possible move from the current state of the chess board.

    """

    @abstractmethod
    def get_best_move(self, state: Any) -> Any:
        """
        Returns the best possible move from the current state of the chess board.
        """
        pass
