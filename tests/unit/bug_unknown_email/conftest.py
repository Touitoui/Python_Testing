"""
Fixtures for testing unknown email login handling.
"""
import pytest
import json
from server import app as flask_app, loadClubs, loadCompetitions


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test_secret'
    
    # Reset data from JSON files for each test
    flask_app.clubs = loadClubs()
    flask_app.competitions = loadCompetitions()
    
    yield flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def valid_club_email():
    """Return a valid club email from the JSON data."""
    clubs = loadClubs()
    return clubs[0]['email']


@pytest.fixture
def invalid_emails():
    """Return a list of invalid email formats and non-existent emails."""
    return [
        'nonexistent@example.com',
        'invalid.email@nowhere.com',
        'fake@club.com',
        'wrong@email.com',
        'notinlist@test.com'
    ]


@pytest.fixture
def malformed_emails():
    """Return a list of malformed email strings."""
    return [
        '',  # Empty string
        'not-an-email',
        '@example.com',
        'user@',
        'user @example.com',
        '   ',  # Whitespace only
    ]
