import pytest

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'something_special'
    with server.app.test_client() as client:
        yield client


def test_club_points_board(client):
    response = client.get("/clubs")
    assert response.status_code == 200
    assert b"<title>Clubs Board || GUDLFT</title>" in response.data
