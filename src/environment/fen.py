from typing_extensions import override
from typing import Any
import chess

from src.environment.environment import Environment

fen = str

class Fen(Environment):
    """Implements an environment that intakes fen strings, and validates them as real chessboards

    This can be anything, as long as it can validate chessboard states and be converted to a fen string and back.
    """

    def to_env(self, repr_state: fen) -> Any:
        """
        Converts a fen string to the environment

        NB: Any should be replaced with the actual type of the environment state

        Args:
            repr_state (fen): The fen string to convert to the given Environment

        Returns:
            Any: The environment state
        """

        if len(repr_state.split()) != 6:
            return False
        try:
            print(chess.Board().set_fen(repr_state))
            return chess.Board().set_fen(repr_state)
        except:
            print(repr_state)
            print("Invalid FEN string")
            return False

    def is_valid(self, state: fen) -> bool:
        """
        Checks if the fens string is a valid chessboard state

        Args:
            state (fen): The fen string to Check

        Returns:
            bool: True if the state is a valid chessboard state, False otherwise
        """

        return self.to_env(state) == None

    @override
    def to_fen(self, state: fen) -> fen:
        """NOT NEEDED"""
        fen: str = state
        return fen
