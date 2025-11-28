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
def large_competition():
    """Create a competition with plenty of places available."""
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "name": "Large Competition",
        "date": future_date,
        "numberOfPlaces": "50"
    }


@pytest.fixture
def sample_club():
    """Return a sample club from the loaded data."""
    return server.clubs[0] if server.clubs else {
        "name": "Test Club",
        "email": "test@touitoui.com",
        "points": "42"
    }
