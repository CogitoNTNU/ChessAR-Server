import subprocess

def get_best_move(fen):
    # Start LCZero as a subprocess
    lc0 = subprocess.Popen(
        ["lc0"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )

    # Send UCI initialization commands
    lc0.stdin.write("uci\n")
    lc0.stdin.write("isready\n")
    lc0.stdin.flush()

    # Send FEN position
    lc0.stdin.write(f"position fen {fen}\n")
    lc0.stdin.write("go movetime 1000\n")  # 1 second thinking time
    lc0.stdin.flush()

    # Read output
    best_move = None
    while True:
        line = lc0.stdout.readline().strip()
        if "bestmove" in line:
            best_move = line.split()[1]  # Extract move
            break

    lc0.stdin.write("quit\n")
    lc0.stdin.flush()
    lc0.terminate()

    return best_move

# Example Usage
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position
best_move = get_best_move(fen)
print(f"Best move: {best_move}")
