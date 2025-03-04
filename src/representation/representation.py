from abc import ABC, abstractmethod
from typing import Union
from environment.environment import Environment

"""
This module implements the representation layer of the overall architecture.
"""


class Representation(ABC):
    """
    This interface defines how all representation layer should work.

    The representation layer is responsible for inputing human understandable information about the chess state (streams or static images) from the viewport and outputing a state that is understandable and representable in code.

    The representation layer inputs a environment to use as a base for the representation. The environment is responsible for making the states computed by the representation layer follow the ruleset of the environment.

    The representation layer must implement the following methods:
    - `compute()`: Takes the input from the viewport and returns the state of the chess board.
    - `get_state()`: Returns the current state of the chess board.

    As how the representation layer should work is dependent on the implementation, the `get_state()` method is left abstract.
    You are free to implement any missing methods you see fit.
    """

    def __init__(self, environment: Environment) -> None:
        self.environment = environment

    @abstractmethod
    def compute(self, input):
        """
        Takes the input from the viewport and returns the state of the chess board.

        input - the stream or image input from the viewport.
        """
        pass

    @abstractmethod
    def get_state(self, abstract) -> Union[str, None]:
        """
        Returns the current state of the chess board as a fen string.

        abstract - the stream or image input from the viewport.
        """
        env_state = self.environment.to_env(input)

        if not self.environment.is_valid(env_state):
            return None

        return self.environment.to_fen(env_state)
