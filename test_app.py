import pytest
import json
from unittest.mock import patch, MagicMock
from myapp.app import create_app
from myapp.config import TestingConfig


@pytest.fixture
def app():
    """Create and configure a test app instance."""
    app = create_app(TestingConfig)
    return app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def mock_db():
    """Mock database engine and connection."""
    with patch('myapp.app.api.routes.get_db') as mock_get_db:
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_engine.connect.return_value.__enter__.return_value = mock_conn
        mock_get_db.return_value = mock_engine
        yield mock_conn


def test_api_stations_returns_list(client, mock_db):
    """Test that /api/stations returns a list of stations."""
    # Mock the database query result with row-like objects.
    row1 = MagicMock()
    row1._mapping = {'number': 1, 'name': 'Station 1', 'address': 'Address 1'}
    row2 = MagicMock()
    row2._mapping = {'number': 2, 'name': 'Station 2', 'address': 'Address 2'}
    mock_db.execute.return_value = [row1, row2]

    response = client.get('/stations')  # Correct path
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'stations' in data
    assert isinstance(data['stations'], list)
    assert len(data['stations']) == 2
    assert data['stations'][0]['number'] == 1
    assert data['stations'][1]['name'] == 'Station 2'


@patch('myapp.app.main.routes.requests.get')
@patch('myapp.app.main.routes.bike_model', new_callable=MagicMock)
def test_api_predict_with_valid_data(mock_bike_model, mock_requests_get, client):
    """Test that /predict returns prediction with valid input data."""
    # Mock the model
    mock_bike_model.predict.return_value = [5.7]  # Predicted bikes

    # Mock weather API response
    mock_weather_response = {
        'main': {'temp': 15.0, 'humidity': 60, 'pressure': 1013},
        'weather': [{'description': 'Clear sky', 'icon': '01d'}],
        'wind': {'speed': 3.5}
    }
    mock_requests_get.return_value.json.return_value = mock_weather_response

    # Test data
    test_data = {
        'station_id': 42,
        'date': '2023-10-15',
        'time': '14:30'
    }

    response = client.post('/predict', json=test_data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert 'station_id' in data
    assert 'predicted_bikes' in data
    assert 'availability_status' in data
    assert 'message' in data
    assert data['station_id'] == 42
    assert data['predicted_bikes'] == 5  # int(5.7)
    assert data['availability_status'] == 'Likely available'
    assert data['message'] == 'Success'


@patch('myapp.app.main.routes.requests.get')
@patch('myapp.app.main.routes.bike_model', new_callable=MagicMock)
def test_api_predict_with_different_weather_conditions(mock_bike_model, mock_requests_get, client):
    """Test /predict with different weather parameters."""
    # Mock the model
    mock_bike_model.predict.return_value = [0.5]  # Low prediction

    # Mock cold weather
    mock_weather_response = {
        'main': {'temp': 5.0, 'humidity': 90, 'pressure': 1005},
        'weather': [{'description': 'Rain', 'icon': '10d'}],
        'wind': {'speed': 10.0}
    }
    mock_requests_get.return_value.json.return_value = mock_weather_response

    test_data = {
        'station_id': 1,
        'date': '2023-12-01',
        'time': '08:00'
    }

    response = client.post('/predict', json=test_data)
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['predicted_bikes'] == 0  # max(0, int(0.5))
    assert data['availability_status'] == 'Unlikely available'


@patch('myapp.app.main.routes.requests.get')
@patch('myapp.app.main.routes.joblib.load')
def test_api_predict_missing_fields(mock_joblib_load, mock_requests_get, client):
    """Test /predict with missing required fields."""
    mock_joblib_load.return_value = MagicMock()

    # Missing station_id
    test_data = {
        'date': '2023-10-15',
        'time': '14:30'
    }

    response = client.post('/predict', json=test_data)
    assert response.status_code == 400

    data = json.loads(response.data)
    assert 'error' in data
    assert 'Missing required fields' in data['error']


@patch('myapp.app.main.routes.requests.get')
@patch('myapp.app.main.routes.joblib.load')
def test_api_predict_invalid_date_format(mock_joblib_load, mock_requests_get, client):
    """Test /predict with invalid date/time format."""
    mock_joblib_load.return_value = MagicMock()

    test_data = {
        'station_id': 42,
        'date': 'invalid-date',
        'time': '14:30'
    }

    response = client.post('/predict', json=test_data)
    assert response.status_code == 400

    data = json.loads(response.data)
    assert 'error' in data
    assert 'Invalid format' in data['error']


@patch('myapp.app.main.routes.bike_model', new=None)
def test_api_predict_model_unavailable(client):
    """Test /predict when model is not loaded."""
    test_data = {
        'station_id': 42,
        'date': '2023-10-15',
        'time': '14:30'
    }

    response = client.post('/predict', json=test_data)
    assert response.status_code == 500

    data = json.loads(response.data)
    assert 'error' in data
    assert 'Model unavailable' in data['error']