"""
This is the main file for the project. Everything starts here...
"""

from dataclasses import dataclass
from asyncio import run, sleep


from src.environment.environment import Environment
from src.environment.positional import Chessboard, Positional
from src.model.model import Model
from src.viewport.frame import Frame
from src.viewport.viewport import ViewPort
from src.model.stockfish import Stockfish
from src.representation.representation import Representation
from src.representation.wishbone import WishBone



@dataclass
class Configuration:
    viewport: Frame
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


async def main(callbacks: Configuration) -> None:

    await callbacks.viewport.init_frame()

    for i in range(10):
        print(f"Loop {i}")
        try:
            image = await callbacks.viewport.get_output()
            image.show()

            chessboard: Chessboard = callbacks.representation.compute(image)

            if chessboard is None:
                await callbacks.viewport.write_to_frame("Picture was bad.")
                await callbacks.viewport.write_to_frame("Taking new picture.")
                continue

            if not callbacks.environment.is_valid(chessboard):
                raise ValueError("Invalid chessboard state")

            fen: str = callbacks.environment.to_fen(chessboard)
            print(f"FEN: {fen} \n")

            best_move = callbacks.model.get_best_move(fen)
            print(f"Best move: {best_move} \n")

            if best_move is None:
                await callbacks.viewport.write_to_frame("Invalid FEN string.")
            else:
                await callbacks.viewport.write_to_frame(best_move)

        except Exception as e:
            print(f"Loop {i}: Caught exception: {e}")
            await callbacks.viewport.write_to_frame("Error occurred.")

    #     await sleep(2.0)
    #     await callbacks.viewport.write_to_frame("Taking new picture.")
    # else:
    #     await callbacks.viewport.write_to_frame("Finished.")
    #     await callbacks.viewport.frame.disconnect()


if __name__ == "__main__":
    callbacks = setup()
    run(main(callbacks))
