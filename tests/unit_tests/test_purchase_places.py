import json
import pytest

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'something_special'
    with server.app.test_client() as client:
        yield client


def test_find_competions():

    form_data = {"competition": "Fall Classic"}
    expected_result = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }

    assert server.find_competition(form_data) == expected_result


def test_find_clubs():

    form_data = {"club": "Iron Temple"}
    expected_result = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    assert server.find_club(form_data) == expected_result


def test_validate_booking_conditions():
    assert server.validate_booking_conditions(5)
    assert not server.validate_booking_conditions(13)


def test_reduce_places_in_competition():

    competition = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
    
    places = 10
    server.reduce_places_in_competition(competition, 10)
    expected_places_left = 3

    assert competition["numberOfPlaces"] == expected_places_left


def test_reduce_club_points():

    club = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    places = 3
    server.reduce_club_points(club, places)
    expected_points_left = 1

    assert club["points"] == expected_points_left


def test_purchase_places(client):

    form_data = {"competition": "Fall Classic", "club": "Iron Temple", "places": "3"}

    response = client.post("/purchasePlaces", data=form_data)

    assert response.status_code == 200


def test_purchase_places_with_invalid_data(client):

    invalid_data = "invalid data"

    response = client.post("/purchasePlaces", data=invalid_data)

    assert response.status_code == 400












