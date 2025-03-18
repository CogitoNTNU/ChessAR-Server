from src.model.stockfish import Stockfish


def test_get_best_move_function():
    """Tests if the get_best_move method returns a string"""
    stockfish: Stockfish = Stockfish()

    # Test with a valid state
    result = stockfish.get_best_move(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )
    assert isinstance(result, str), "get_best_move should return a string value"
