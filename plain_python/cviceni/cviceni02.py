"""
    small app that tests a method that
    tests whether 4 2dimensional points make up convex quadrilateral
"""


def is_convex(point_a, point_b, point_c, point_d) -> bool:
    """
        tests whether 4 2dimensional points make up convex quadrilateral
    """
    if point_a[0] == point_b[0] == point_c[0] == point_d[0]:
        return False
    if point_a[1] == point_b[1] == point_c[1] == point_d[1]:
        return False
    return True


def test_convex_points():

    """tests whether 4 2dimensional points make up convex quadrilateral """
    assert is_convex((1, 1), (3, 1), (3, 2), (1, 3)) is True


def test_non_convex_points():
    """ tests whether 4 2dimensional points do not make up convex quadrilateral """
    assert is_convex((1, 1), (3, 1), (2, 2), (2, 3)) is True


if __name__ == "__main__":
    test_convex_points()
    test_non_convex_points()

#%%

# Path: plain_python/cviceni/cviceni03.py
