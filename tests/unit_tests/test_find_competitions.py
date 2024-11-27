import pytest

from server import find_competition


def test_find_competition():

    competition = "Spring Festival"
    expected_result = {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
        "past": True
    }

    assert find_competition(competition) == expected_result


def test_find_invalid_competition():
    competition = "Invalid competition"
    with pytest.raises(IndexError):
        find_competition(competition)
