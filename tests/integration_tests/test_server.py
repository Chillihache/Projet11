import pytest
from flask import session

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'something_special'
    with server.app.test_client() as client:
        yield client


def test_integration_server(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>GUDLFT Registration</title>" in response.data

    response = client.post("/showSummary", data={"email": "john@simplylift.co"})
    assert response.status_code == 200
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data
    assert session.get("name") == "Simply Lift"

    response = client.get("book/Fall Classic/Simply Lift")
    assert response.status_code == 200
    assert b"<title>Booking for Fall Classic || GUDLFT</title>" in response.data

    form_data = {"club": "Simply Lift", "competition": "Fall Classic", "places": 5}
    response = client.post("/purchasePlaces", data=form_data)
    assert response.status_code == 200
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data

    club = next(club for club in server.clubs if club["name"] == "Simply Lift")
    assert club["points"] == 8

    competition = next(comp for comp in server.competitions if comp["name"] == "Fall Classic")
    assert competition["numberOfPlaces"] == 8

    response = client.get("/clubs")
    assert response.status_code == 200
    assert b"<title>Clubs Board || GUDLFT</title>" in response.data

    response = client.get("/backHome")
    assert response.status_code == 200
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data

    response = client.get("logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>GUDLFT Registration</title>" in response.data
    assert not session.get("name")





