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
def club_with_10_points():
    """Create a club with 10 points."""
    return {
        "name": "Medium Club",
        "email": "medium@club.com",
        "points": "10"
    }


@pytest.fixture
def club_with_0_points():
    """Create a club with no points."""
    return {
        "name": "No Points Club",
        "email": "zero@club.com",
        "points": "0"
    }


@pytest.fixture
def standard_competition():
    """Create a standard competition with plenty of places."""
    future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    return {
        "name": "Standard Competition",
        "date": future_date,
        "numberOfPlaces": "25"
    }
