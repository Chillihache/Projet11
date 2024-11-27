from io import StringIO

from server import load_competitions


def test_load_competitions(monkeypatch):
    mock_data = '{"competitions": [{"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},'\
                '{"name": "Fall Classic", "date": "2025-10-22 13:30:00", "numberOfPlaces": "13"}]}'

    mock_file = StringIO(mock_data)

    def mock_open(*args, **kwargs):
        return mock_file

    monkeypatch.setattr("builtins.open", mock_open)

    competitions = load_competitions()
    assert len(competitions) == 2
    assert competitions[0]["name"] == "Spring Festival"
    assert competitions[0]["past"]
    assert not competitions[1]["past"]
