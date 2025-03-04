"""
This is the main file for the project. Everything starts here...
"""

from representation.representation import Representation
from environment.environment import Environment
from model.model import Model
from viewport.viewport import ViewPort
from time import sleep


class Server:
    def __init__(
        self,
        representation: Representation,
        environment: Environment,
        model: Model,
        viewport: ViewPort,
    ) -> None:
        self.representation = representation
        self.environment = environment
        self.model = model
        self.viewport = viewport

    def run(self) -> None:
        while True:
            vp_out = self.viewport.get_output()
            abstract = self.representation.compute(vp_out)
            state = self.representation.get_state(abstract)
            if state is None:
                raise Exception("Invalid state")
            best_move = self.model.get_best_move(state)
            print("Best move:", best_move)
            sleep(1)


def main() -> None:
    server: Server = Server()
    print("Starting server...")
    server.run()


if __name__ == "__main__":
    main()
