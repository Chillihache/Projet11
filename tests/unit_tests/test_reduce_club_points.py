from server import reduce_club_points


def test_reduce_club_points():

    club = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    places = 3
    reduce_club_points(club, places)
    expected_points_left = 1

    assert club["points"] == expected_points_left
