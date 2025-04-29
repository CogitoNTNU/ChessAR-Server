"""
This is the main file for the project. Everything starts here...
"""

from asyncio import sleep
from dataclasses import dataclass

from frame_ble.frame_ble import asyncio
from src.environment.environment import Environment
from src.environment.positional import Chessboard, Positional
from src.model.model import Model
from src.viewport.frame import Frame
from src.viewport.viewport import ViewPort
from src.model.stockfish import Stockfish
from src.representation.representation import Representation
from src.representation.wishbone import WishBone
from src.viewport.snapshot import SnapShot, ViewPortImage
from src.viewport.write_to_glasses import FrameController

from time import sleep

@dataclass
class Configuration:
    viewport: ViewPort
    environment: Environment
    representation: Representation
    model: Model

def setup() -> Configuration:
    """Setup the environment, representation and model"""

    viewport: ViewPort = Frame()
    environment: Environment = Positional()
    repr: Representation = WishBone(environment)
    model: Model = Stockfish()

    return Configuration(viewport=viewport, environment=environment, representation=repr, model=model)

def main() -> None:
    callbacks = setup()
    image = asyncio.run(callbacks.viewport.get_output())
    image.show()

    chessboard: Chessboard = callbacks.representation.compute(image)
    
    if not callbacks.environment.is_valid(chessboard):
        raise ValueError("Invalid chessboard state")

    fen: str = callbacks.environment.to_fen(chessboard)
    
    print(f"FEN: {fen} \n")
    
    best_move = callbacks.model.get_best_move(fen)

    print(f"Best move: {best_move} \n")
    # asyncio.run(callbacks.viewport.send_bestmove(best_move))

    


if __name__ == "__main__":
    main()
