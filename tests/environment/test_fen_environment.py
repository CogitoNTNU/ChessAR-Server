import pytest

from src.environment.fen_environment import FenEnvironment


def test_is_to_fen_implemented():
    """Tests if the to_fen method is implemented"""
    environment: FenEnvironment = FenEnvironment()
    actual: str = "4kb1r/p4ppp/4q3/8/8/1B6/PPP2PPP/2KR4"
    fen_string: str = environment.to_fen(actual)
    assert fen_string == actual


def test_is_to_env_implemented():
    """Tests if the is_valid method is implemented and doesn't raise exceptions"""
    environment: FenEnvironment = FenEnvironment()

    # Try calling the method with a valid FEN string
    try:
        result = environment.is_valid(
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        )
        # Check that it returns a boolean value
        assert isinstance(result, bool)
    except NotImplementedError:
        pytest.fail("is_valid method is not implemented")
    except Exception as e:
        pytest.fail(f"is_valid method raised an unexpected exception: {e}")


def test_is_is_valid_implemented():
    """Tests if the is_valid method returns a boolean value"""
    environment: FenEnvironment = FenEnvironment()

    # Test with a valid FEN string
    result_valid = environment.is_valid(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    )
    assert isinstance(result_valid, bool), "is_valid should return a boolean value"

    # Test with an invalid FEN string
    result_invalid = environment.is_valid("invalid fen string")
    assert isinstance(
        result_invalid, bool
    ), "is_valid should return a boolean value even for invalid input"


def test_is_valid_with_valid_fen_string():
    """Tests if is_valid returns True for a valid FEN string"""
    environment: FenEnvironment = FenEnvironment()
    valid_fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    assert environment.is_valid(valid_fen) is True


def test_is_valid_with_valid_fen_string_black_to_move():
    """Tests if is_valid returns True for a valid FEN string with black to move"""
    environment: FenEnvironment = FenEnvironment()
    valid_fen: str = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    assert environment.is_valid(valid_fen) is True


def test_is_valid_with_valid_fen_string_midgame():
    """Tests if is_valid returns True for a valid midgame position"""
    environment: FenEnvironment = FenEnvironment()
    valid_fen: str = (
        "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4"
    )
    assert environment.is_valid(valid_fen) is True


def test_is_valid_with_invalid_fen_string_wrong_format():
    """Tests if is_valid returns False for a FEN string with wrong format"""
    environment: FenEnvironment = FenEnvironment()
    invalid_fen: str = (
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"  # Missing additional fields
    )
    assert environment.is_valid(invalid_fen) is False


def test_is_valid_with_invalid_fen_string_wrong_piece_placement():
    """Tests if is_valid returns False for a FEN string with invalid piece placement"""
    environment: FenEnvironment = FenEnvironment()
    invalid_fen: str = (
        "rnbqkbnr/ppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Missing a 'p' in the second rank
    )
    assert environment.is_valid(invalid_fen) is False


def test_is_valid_with_invalid_fen_string_wrong_active_color():
    """Tests if is_valid returns False for a FEN string with invalid active color"""
    environment: FenEnvironment = FenEnvironment()
    invalid_fen: str = (
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR x KQkq - 0 1"  # 'x' instead of 'w' or 'b'
    )
    assert environment.is_valid(invalid_fen) is False
