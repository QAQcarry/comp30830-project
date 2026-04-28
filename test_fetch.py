import json
from unittest.mock import patch, MagicMock


def test_weather_fetch_success(client, monkeypatch):
    """Test the weather fetch route returns parsed Dublin weather data."""
    monkeypatch.setenv("OPENWEATHER_API_KEY", "dummy-key")

    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "main": {"temp": 15.0, "feels_like": 14.0, "humidity": 55},
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "wind": {"speed": 3.2},
    }

    with patch("myapp.app.api.routes.requests.get", return_value=mock_response):
        response = client.get("/weather")

    assert response.status_code == 200
    data = response.get_json()
    assert "weather" in data
    assert isinstance(data["weather"], list)
    assert data["weather"][0]["temp"] == 15.0
    assert data["weather"][0]["description"] == "Clear Sky"
    assert data["weather"][0]["humidity"] == 55


def test_weather_fetch_fallback_on_error(client, monkeypatch):
    """Test the weather endpoint falls back when the external API fails."""
    monkeypatch.setenv("OPENWEATHER_API_KEY", "dummy-key")

    def raise_request_error(*args, **kwargs):
        raise RuntimeError("weather API failure")

    with patch("myapp.app.api.routes.requests.get", side_effect=raise_request_error):
        response = client.get("/weather")

    assert response.status_code == 200
    data = response.get_json()
    assert "weather" in data
    assert data["weather"][0]["description"] == "Unavailable"
    assert data["weather"][0]["temp"] == 12.5
