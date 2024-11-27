from server import validate_booking_conditions


def test_validate_booking_conditions():

    competition = {
        "name": "Fall Classic",
        "date": "2025-10-22 13:30:00",
        "numberOfPlaces": "13"
    }

    club = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "7"
    }

    assert validate_booking_conditions(club, competition, 5)
    assert not validate_booking_conditions(club, competition, 13)
    