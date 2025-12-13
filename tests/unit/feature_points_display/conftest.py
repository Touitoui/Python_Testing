"""
Fixtures for testing points display feature.
"""
import pytest
import json
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
def sample_clubs():
    """Return sample clubs with different point values."""
    return [
        {'name': 'Club A', 'email': 'club.a@test.com', 'points': '10'},
        {'name': 'Club B', 'email': 'club.b@test.com', 'points': '25'},
        {'name': 'Club C', 'email': 'club.c@test.com', 'points': '0'},
        {'name': 'Club D', 'email': 'club.d@test.com', 'points': '50'},
    ]


@pytest.fixture
def setup_clubs(app, sample_clubs):
    """Setup test clubs."""
    import server
    server.clubs = sample_clubs
    return app
