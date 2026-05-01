import json
from unittest.mock import patch, MagicMock


def test_stations_route_returns_station_list(client):
    """Verify the stations endpoint returns JSON station data."""
    row1 = MagicMock()
    row1._mapping = {"number": 1, "name": "Station 1", "address": "Address 1"}
    row2 = MagicMock()
    row2._mapping = {"number": 2, "name": "Station 2", "address": "Address 2"}

    with patch("myapp.app.api.routes.get_db") as mock_get_db:
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_get_db.return_value = mock_engine
        mock_conn.execute.return_value = [row1, row2]

        response = client.get("/stations")

    assert response.status_code == 200
    data = response.get_json()
    assert "stations" in data
    assert len(data["stations"]) == 2
    assert data["stations"][0]["number"] == 1
    assert data["stations"][1]["name"] == "Station 2"


def test_predict_route_returns_prediction_with_mocked_weather(client, monkeypatch):
    """Verify predict route works with a mocked external weather API."""
    mock_bike_model = MagicMock()
    mock_bike_model.predict.return_value = [4.7]

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "main": {"temp": 16.0, "humidity": 60, "pressure": 1015},
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "wind": {"speed": 2.1},
    }

    monkeypatch.setenv("OPENWEATHER_API_KEY", "dummy-key")

    with patch("myapp.app.main.routes.requests.get", return_value=mock_response), \
         patch("myapp.app.main.routes.bike_model", mock_bike_model):
        response = client.post(
            "/predict",
            json={"station_id": 5, "date": "2024-05-01", "time": "09:30"},
        )

    assert response.status_code == 200
    data = response.get_json()
    assert data["station_id"] == 5
    assert data["predicted_bikes"] == 4
    assert data["availability_status"] == "Likely available"
    assert data["message"] == "Success"


def test_predict_route_falls_back_when_weather_api_fails(client, monkeypatch):
    """Verify predict route uses fallback values when weather API fails."""
    mock_bike_model = MagicMock()
    mock_bike_model.predict.return_value = [0.2]
    monkeypatch.setenv("OPENWEATHER_API_KEY", "dummy-key")

    def raise_error(*args, **kwargs):
        raise RuntimeError("weather failure")

    with patch("myapp.app.main.routes.requests.get", side_effect=raise_error), \
         patch("myapp.app.main.routes.bike_model", mock_bike_model):
        response = client.post(
            "/predict",
            json={"station_id": 7, "date": "2024-12-01", "time": "14:00"},
        )

    assert response.status_code == 200
    data = response.get_json()
    assert data["predicted_bikes"] == 0
    assert data["availability_status"] == "Unlikely available"


def test_predict_route_returns_400_for_missing_fields(client):
    response = client.post("/predict", json={"date": "2024-05-01", "time": "09:30"})
    assert response.status_code == 400
    data = response.get_json()
    assert "Missing required fields" in data["error"]
