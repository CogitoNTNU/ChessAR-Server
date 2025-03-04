from abc import ABC, abstractmethod
from typing import List

"""
This implements a standard environment interface to be used as a base for all game environments.
"""


class Environment(ABC):
    """
    This interface defines how all environment layer should work.

    The environment layer is responsible for inputing the representation layer output and converting it into a usable state of the environment.

    The environment layer must implement the following methods:
    - `to_env()`: Takes the representation output and returns as a state of the environment.
    - `is_valid()`: Takes an action and returns whether the action is valid or not.
    - `to_fen()`: Returns the current state of the game as a fen string.

    """

    @abstractmethod
    def to_env(self, repr_state) -> List[List[object]]:
        """
        Takes a state and returns the state as a list of lists.
        """
        pass

    @abstractmethod
    def is_valid(self, state: List[List[object]]) -> bool:
        """
        Takes a state and checks if the state is valid for the environment.
        """
        pass

    @abstractmethod
    def to_fen(self, state: List[List[object]]) -> str:
        """
        Returns the current state of the game as a fen string.
        """
        pass
