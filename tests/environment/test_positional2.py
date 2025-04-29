# tests/test_positional_env.py
import pytest
import numpy as np
import cv2
from src.environment.positional2 import (
    order_corners, get_perspective_transform, warp_point,
    Positional, Corners, PiecePositions, PositionalParams
)


def test_order_corners_rectangular():
    # define corners of a rectangle with some jitter
    inputs = [Corners(x=1, y=1, width=0, height=0),  # tl
              Corners(x=5, y=1, width=0, height=0),  # tr
              Corners(x=5, y=3, width=0, height=0),  # br
              Corners(x=1, y=3, width=0, height=0)]
    ordered = order_corners(inputs)
    # should map to these exact points
    expected = np.array([[1,1],[5,1],[5,3],[1,3]], dtype="float32")
    assert np.allclose(ordered, expected)


def test_perspective_transform_identity():
    # feed ordered points equal to destination corners for board_size=10
    ordered = np.array([[0,0],[9,0],[9,9],[0,9]], dtype="float32")
    M = get_perspective_transform(ordered, board_size=10)
    # any corner should map to itself
    pts = [ (0,0), (9,0), (9,9), (0,9) ]
    for pt in pts:
        xw, yw = warp_point(pt, M)
        assert pytest.approx(pt[0], abs=1e-6) == xw
        assert pytest.approx(pt[1], abs=1e-6) == yw

def test_to_fen_simple():
    board = [
        ['r','n','b','q','k','b','n','r'],
        ['p']*8,
        ['']*8,
        ['']*8,
        ['']*8,
        ['']*8,
        ['P']*8,
        ['R','N','B','Q','K','B','N','R'],
    ]
    pos = Positional()
    fen = pos.to_fen(board)
    assert fen.startswith('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    assert fen.endswith(' w - - 0 0')


def test_to_env_and_fen_center_piece():
    # square board from (0,0) to (8,8), piece at center
    corners = [Corners(x=0,y=0,width=0,height=0), Corners(x=8,y=0,width=0,height=0),
               Corners(x=8,y=8,width=0,height=0), Corners(x=0,y=8,width=0,height=0)]
    piece = PiecePositions(x=4,y=4,piece='Q',probability=0.9)
    params = PositionalParams(corner_positions=corners, piece_positions=[piece])
    pos = Positional()
    board = pos.to_env(params)
    # center maps to square (4,4) => row 4, col 4 => e4 (but board uses row index)
    assert board[3][3] == 'Q'
    fen = pos.to_fen(board)
    # row 4 is fifth rank: ranks:0->8th,4->4th; so FEN part for rank 4 should have Q at 5th file
    ranks = fen.split(' ')[0].split('/')
    assert ranks[3][1] == 'Q'
