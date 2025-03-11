from model.model import Model
from typing import List
import requests

class StockfishModel(Model):
    def __init__(self, depth: int = 20):
        super().__init__()
        self.url = "https://chess-api.com/v1"
        self.depth = depth

    def get_best_move(self, fen: str) -> List[str]:
        headers = {"fen": fen,
                "depth": self.depth
            }
        ans = requests.post(self.url, json=headers)
        return ans.json()["move"]

