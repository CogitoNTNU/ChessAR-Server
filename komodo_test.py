import subprocess

def get_best_move(fen):
    # Start LCZero as a subprocess
    dragon = subprocess.Popen(
        ["../Chess_engines/dragon_05e2a7/OSX/dragon-osx"],
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
    dragon.stdin.write("go movetime 1000\n")  # 1 second thinking time
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

# Example Usage
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position
best_move = get_best_move(fen)
print(f"Best move: {best_move}")
