import pytest

from server import find_club


def test_find_club():

    club = "Iron Temple"
    expected_result = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    assert find_club(club) == expected_result


def test_find_invalid_club():
    club = "Invalid club"
    with pytest.raises(IndexError):
        find_club(club)
