from src.model.model import Model
from typing import List, Literal
import requests


class Stockfish(Model):
    type: Literal["stockfish_model"] = "stockfish_model"

    def __init__(self, depth: int = 20):
        super().__init__()
        self.url = "https://chess-api.com/v1"
        self.depth = depth

    def get_best_move(self, state: str) -> List[str]:
        headers = {"fen": state, "depth": self.depth}
        ans = requests.post(self.url, json=headers)
        print(ans.json())
        try:
            return ans.json()["move"]
        except:
            print(f"Could not evaluate position {state}!")

            
