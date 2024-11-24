import pytest
from io import StringIO
from flask import session

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'something_special'
    with server.app.test_client() as client:
        yield client


def test_load_clubs(monkeypatch):
    mock_data = '{"clubs":[{"name":"Simply Lift", "email":"john@simplylift.co", "points":"13"}]}'

    mock_file = StringIO(mock_data)

    def mock_open(*args, **kwargs):
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)

    clubs = server.load_clubs()
    assert len(clubs) == 1
    assert clubs[0]["email"] == "john@simplylift.co"


def test_load_competitions(monkeypatch):
    mock_data = '{"competitions": [{"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},'\
                '{"name": "Fall Classic", "date": "2025-10-22 13:30:00", "numberOfPlaces": "13"}]}'

    mock_file = StringIO(mock_data)

    def mock_open(*args, **kwargs):
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)

    competitions = server.load_competitions()
    assert len(competitions) == 2
    assert competitions[0]["name"] == "Spring Festival"
    assert competitions[0]["past"]
    assert not competitions[1]["past"]


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>GUDLFT Registration</title>" in response.data


def test_show_summary(client):

    form_data = {"email": "john@simplylift.co"}
    response = client.post("/showSummary", data=form_data)

    assert response.status_code == 200
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data


def test_show_summary_email_not_found(client):
    form_data = {"email": "invalid@email.com"}
    response = client.post("/showSummary", data=form_data)

    assert response.status_code == 200
    assert b"<title>GUDLFT Registration</title>" in response.data
    assert b"No account found" in response.data


def test_find_club():

    club = "Iron Temple"
    expected_result = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    assert server.find_club(club) == expected_result


def test_find_invalid_club():
    club = "Invalid club"
    with pytest.raises(IndexError):
        server.find_club(club)


def test_find_competition():

    competition = "Fall Classic"
    expected_result = {
        "name": "Fall Classic",
        "date": "2025-10-22 13:30:00",
        "numberOfPlaces": "13",
        "past": False
    }

    assert server.find_competition(competition) == expected_result


def test_find_invalid_competition():
    competition = "Invalid competition"
    with pytest.raises(IndexError):
        server.find_competition(competition)


def test_book(client):
    response = client.get("book/Spring%20Festival/Iron%20Temple")
    assert response.status_code == 200


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

    assert server.validate_booking_conditions(club, competition, 5)
    assert not server.validate_booking_conditions(club, competition, 13)


def test_reduce_places_in_competition():

    competition = {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13"
    }
    
    places = 10
    server.reduce_places_in_competition(competition, places)
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


def test_clubs_points_board(client):
    with client.session_transaction() as session:
        session["name"] = "Iron Temple"

    response = client.get("/clubs")

    assert response.status_code == 200
    assert b"<title>Clubs Board || GUDLFT</title>" in response.data


def logout(client):
    response = client.get("/logout")
    assert response.status_code == 200
    assert b"<title>GUDLFT Registration</title>" in response.data
