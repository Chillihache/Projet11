import pytest

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'something_special'
    with server.app.test_client() as client:
        yield client


def test_purchase_places(client):

    form_data = {"competition": "Fall Classic", "club": "Iron Temple", "places": "3"}

    response = client.post("/purchasePlaces", data=form_data)

    assert response.status_code == 200


def test_purchase_places_with_invalid_data(client):
    invalid_data = "invalid data"
    response = client.post("/purchasePlaces", data=invalid_data)

    assert response.status_code == 400
