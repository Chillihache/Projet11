from server import reduce_places_in_competition


def test_reduce_places_in_competition():
    competition = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }

    places = 10
    reduce_places_in_competition(competition, places)
    expected_places_left = 3

    assert competition["numberOfPlaces"] == expected_places_left
