from io import StringIO

from server import load_clubs


def test_load_clubs(monkeypatch):
    mock_data = '{"clubs":[{"name":"Simply Lift", "email":"john@simplylift.co", "points":"13"}]}'

    mock_file = StringIO(mock_data)

    def mock_open(*args, **kwargs):
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)

    clubs = load_clubs()
    assert len(clubs) == 1
    assert clubs[0]["email"] == "john@simplylift.co"
