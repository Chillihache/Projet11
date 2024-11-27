import pytest

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'something_special'
    with server.app.test_client() as client:
        yield client


def test_book(client):
    response = client.get("book/Spring%20Festival/Iron%20Temple")
    assert response.status_code == 200
    