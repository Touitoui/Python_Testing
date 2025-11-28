"""Pytest configuration and fixtures for testing the GUDLFT application."""
import pytest
import json
from datetime import datetime, timedelta
import server


@pytest.fixture
def app():
    """Create and configure a test instance of the Flask app."""
    server.app.config['TESTING'] = True
    server.app.config['SECRET_KEY'] = 'test_secret_key'
    
    # Reset data to initial state for each test
    server.clubs = server.loadClubs()
    server.competitions = server.loadCompetitions()
    
    return server.app


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()


@pytest.fixture
def competition_with_5_places():
    """Create a competition with only 5 places available."""
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "name": "Small Competition",
        "date": future_date,
        "numberOfPlaces": "5"
    }


@pytest.fixture
def competition_with_10_places():
    """Create a competition with 10 places available."""
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "name": "Medium Competition",
        "date": future_date,
        "numberOfPlaces": "10"
    }


@pytest.fixture
def competition_with_1_place():
    """Create a competition with only 1 place available."""
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "name": "Almost Full Competition",
        "date": future_date,
        "numberOfPlaces": "1"
    }


@pytest.fixture
def sample_club():
    """Return a sample club from the loaded data."""
    return server.clubs[0] if server.clubs else {
        "name": "Test Club",
        "email": "test@touitoui.com",
        "points": "42"
    }
