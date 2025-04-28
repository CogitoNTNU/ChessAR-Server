import pytest
import numpy as np
from unittest.mock import patch, MagicMock

from src.environment.positional import Positional, Corners, PiecePositions, PositionalParams


@pytest.fixture
def simple_corners():
    return [
        Corners(x=0, y=0, width=0, height=0),
        Corners(x=0, y=1, width=0, height=0),
        Corners(x=1, y=0, width=0, height=0),
        Corners(x=1, y=1, width=0, height=0),
    ]

@pytest.fixture
def sample_piece_positions():
    return [
        PiecePositions(x=0.1, y=0.1, piece='r', probability=0.95),
        PiecePositions(x=0.9, y=0.1, piece='n', probability=0.95),
        PiecePositions(x=0.1, y=0.9, piece='b', probability=0.95),
    ]

@pytest.fixture
def positional_env():
    return Positional()

def test_find_transformation_matrix(positional_env, simple_corners):
    matrix = positional_env.find_transformation_matrix(simple_corners)
    assert matrix.shape == (2, 2)
    expected = np.array([[1, 0], [0, 1]])
    result = positional_env.transform_to_board_space_vector(matrix, np.array([1, 0]))
    np.testing.assert_almost_equal(result, np.array([0, 1])) # May need to check this some more

def test_transform_to_board_space_vector(positional_env):
    matrix = np.array([[1, 0], [0, 1]])
    vec = np.array([0.5, 0.75])
    transformed = positional_env.transform_to_board_space_vector(matrix, vec)
    np.testing.assert_array_equal(transformed, vec)

def test_get_piece_positions_in_board_space(positional_env, simple_corners, sample_piece_positions):
    state = PositionalParams(
        corner_positions=simple_corners,
        piece_positions=sample_piece_positions
    )
    result = positional_env.get_piece_positions_in_board_space(state)
    assert len(result) == 3
    for piece in result:
        assert 0 <= piece.x <= 1
        assert 0 <= piece.y <= 1

def test_to_env(positional_env, simple_corners):
    pieces = [
        PiecePositions(x=0.01, y=0.01, piece='r', probability=1.0),
        PiecePositions(x=0.99, y=0.01, piece='n', probability=1.0),
    ]
    params = PositionalParams(
        corner_positions=simple_corners,
        piece_positions=pieces
    )
    board = positional_env.to_env(params)
    assert isinstance(board, list)
    assert board[0][0] == 'r'
    assert board[0][8 - 1] == 'n'

@patch("src.environment.positional.Fen")
def test_is_valid(mock_fen_class, positional_env, simple_corners):
    mock_fen_instance = MagicMock()
    mock_fen_instance.is_valid.return_value = True
    mock_fen_class.return_value = mock_fen_instance

    board = [["r"] + [""] * 7] + [[""] * 8 for _ in range(7)]
    assert positional_env.is_valid(board)
    mock_fen_instance.is_valid.assert_called_once()

def test_to_fen(positional_env):
    board = [
        ['r', '', '', '', '', '', '', 'n'],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]
    fen = positional_env.to_fen(board)
    assert fen.startswith("r6n")
    assert fen.endswith(" w - - 0 0")