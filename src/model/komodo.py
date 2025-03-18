import subprocess
from typing import List
from src.model.model import Model

class Komodo(Model):
    def __init__(self, movetime: int = 1000):
        super().__init__()
        self.movetime = movetime

    def get_best_move(self, fen: str) -> str:
        # Start Komodo Dragon as a subprocess
        dragon = subprocess.Popen(
            ["src/model/engines/dragon_05e2a7/OSX/dragon-osx"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )

        # Send UCI initialization commands
        dragon.stdin.write("uci\n")
        dragon.stdin.write("isready\n")
        dragon.stdin.flush()

        # Send FEN position
        dragon.stdin.write(f"position fen {fen}\n")
        dragon.stdin.write(f"go movetime {self.movetime}\n")  # 1 second thinking time
        dragon.stdin.flush()

        # Read output
        best_move = None
        while True:
            line = dragon.stdout.readline().strip()
            if "bestmove" in line:
                best_move = line.split()[1]  # Extract move
                break

        dragon.stdin.write("quit\n")
        dragon.stdin.flush()
        dragon.terminate()

        return best_move