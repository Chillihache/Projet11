import pytest

import server


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'something_special'
    with server.app.test_client() as client:
        yield client


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
    