import subprocess
from typing import List
from src.model.model import Model


class Leela(Model):
    def __init__(self, movetime: int = 1000):
        super().__init__()
        self.movetime = movetime

    def get_best_move(self, state: str) -> str:
        # Start LCZero as a subprocess
        leela = subprocess.Popen(
            ["src/model/engines/lc0/0.31.2/libexec/lc0"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )

        # Send UCI initialization commands
        leela.stdin.write("uci\n")
        leela.stdin.write("isready\n")
        leela.stdin.flush()

        # Send FEN position
        leela.stdin.write(f"position fen {state}\n")
        leela.stdin.write(f"go movetime {self.movetime}\n")  # 1 second thinking time
        leela.stdin.flush()

        # Read output
        best_move = None
        while True:
            line = leela.stdout.readline().strip()
            if "bestmove" in line:
                best_move = line.split()[1]  # Extract move
                break

        leela.stdin.write("quit\n")
        leela.stdin.flush()
        leela.terminate()

        return best_move
