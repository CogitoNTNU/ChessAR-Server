import requests

fen = "r1bqk2r/4bppp/p1np1n2/1p1Np1B1/4P3/N7/PPP2PPP/R2QKB1R w KQkq - 2 10"
depth = 20

def get_best_move(fen: str, depth: int) -> list[str]:
    headers = {"fen": fen,
               "depth": depth
           }
    ans = requests.post("https://chess-api.com/v1", json=headers)
    print(ans.text)

get_best_move(fen, depth)
