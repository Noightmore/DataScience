#!/bin/env python
# -*- coding: utf-8 -*-

"""
    small app that tests a method that
    tests whether 4 2dimensional points make up convex quadrilateral
"""

# basically a solution:
# https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle


def sign(point_a, point_b, point_c) -> float:
    """
    : computes determinant
    :param point_a:
    :param point_b:
    :param point_c:
    :return:
    """
    return (point_a[0] - point_c[0]) * (point_b[1] - point_c[1]) \
        - (point_b[0] - point_c[0]) * (point_a[1] - point_c[1])


def is_inside_triangle(point_a, point_b, point_c, point_d) -> bool:
    """
    tests whether 4 2dimensional points make up convex quadrilateral
    """
    d_1 = sign(point_d, point_a, point_b)
    d_2 = sign(point_d, point_b, point_c)
    d_3 = sign(point_d, point_c, point_a)

    has_neg = (d_1 < 0) or (d_2 < 0) or (d_3 < 0)
    has_pos = (d_1 > 0) or (d_2 > 0) or (d_3 > 0)

    return not (has_neg and has_pos)


def is_convex(point_a, point_b, point_c, point_d) -> bool:
    """
        loops through all possible combinations of points and checks if they are inside triangle
    """

    if is_inside_triangle(point_a, point_b, point_c, point_d):
        return False
    if is_inside_triangle(point_a, point_b, point_d, point_c):
        return False
    if is_inside_triangle(point_a, point_c, point_d, point_b):
        return False
    if is_inside_triangle(point_b, point_c, point_d, point_a):
        return False

    return True


def test_convex_points():
    """tests whether 4 2dimensional points make up convex quadrilateral """
    assert is_convex((1, 1), (3, 1), (3, 2), (1, 3)) is True
    assert is_convex((-1.0, -1.0), (1.0, -1.0), (1.0, 1.0), (-1.0, 1.0)) is True
    assert is_convex((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)) is True
    assert is_convex((0.0, 0.0), (1.1, 0.1), (0.9, 0.8), (0.1, 0.9)) is True


def test_non_convex_points():
    """ tests whether 4 2dimensional points do not make up convex quadrilateral """
    assert is_convex((1, 1), (3, 1), (2, 2), (2, 3)) is False
    assert is_convex((0.0, 0.0), (1.0, 0.0), (0.3, 0.3), (0.0, 1.0)) is False
    assert is_convex((0.0, 0.0), (0.2, 0.7), (1.0, 1.0), (0.0, 1.0)) is False
    assert is_convex((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.7, 0.3)) is False
    assert is_convex((0.7, 0.8), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)) is False
    assert is_convex((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 0.0)) is False
    assert is_convex((0.0, 0.0), (1.0, 0.0), (1.0, 0.0), (0.0, 0.0)) is False
    assert is_convex((1.0, 0.0), (1.0, 0.0), (1.0, 0.0), (1.0, 0.0)) is False


if __name__ == "__main__":
    test_convex_points()
    test_non_convex_points()

"""
    poznamky k pylintu:
    
    cviceni02.py:46:7: W1114: Positional arguments appear to be out of order (arguments-out-of-order)
    cviceni02.py:48:7: W1114: Positional arguments appear to be out of order (arguments-out-of-order)
    cviceni02.py:50:7: W1114: Positional arguments appear to be out of order (arguments-out-of-order)
    
    argumenty out of order jsou schvalne, aby se testovaly vsechny kombinace

"""
