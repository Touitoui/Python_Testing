"""
Fixtures for integration tests.
"""
import pytest
import json
from datetime import datetime, timedelta
from server import app as flask_app, loadClubs, loadCompetitions


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    import server
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test_secret'
    
    # Reset data from JSON files for each test
    server.clubs = loadClubs()
    server.competitions = loadCompetitions()
    
    yield flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def sample_club():
    """Return a sample club with moderate points."""
    return {
        'name': 'Test Club',
        'email': 'test@touitoui.com',
        'points': '20'
    }


@pytest.fixture
def low_points_club():
    """Return a club with low points."""
    return {
        'name': 'Low Points Club',
        'email': 'low@club.com',
        'points': '3'
    }


@pytest.fixture
def high_points_club():
    """Return a club with high points."""
    return {
        'name': 'Rich Club',
        'email': 'rich@club.com',
        'points': '50'
    }


@pytest.fixture
def zero_points_club():
    """Return a club with zero points."""
    return {
        'name': 'Broke Club',
        'email': 'broke@club.com',
        'points': '0'
    }


@pytest.fixture
def future_competition():
    """Return a competition in the future."""
    future_date = datetime.now() + timedelta(days=30)
    return {
        'name': 'Future Competition',
        'date': future_date.strftime('%Y-%m-%d %H:%M:%S'),
        'numberOfPlaces': '25'
    }


@pytest.fixture
def past_competition():
    """Return a competition in the past."""
    past_date = datetime.now() - timedelta(days=30)
    return {
        'name': 'Past Competition',
        'date': past_date.strftime('%Y-%m-%d %H:%M:%S'),
        'numberOfPlaces': '25'
    }


@pytest.fixture
def limited_places_competition():
    """Return a competition with limited places."""
    future_date = datetime.now() + timedelta(days=15)
    return {
        'name': 'Limited Competition',
        'date': future_date.strftime('%Y-%m-%d %H:%M:%S'),
        'numberOfPlaces': '5'
    }


@pytest.fixture
def setup_test_data(app, sample_club, low_points_club, high_points_club, 
                    zero_points_club, future_competition, past_competition, 
                    limited_places_competition):
    """Setup complete test data with clubs and competitions."""
    import server
    server.clubs = [sample_club, low_points_club, high_points_club, zero_points_club]
    server.competitions = [future_competition, past_competition, limited_places_competition]
    return app
