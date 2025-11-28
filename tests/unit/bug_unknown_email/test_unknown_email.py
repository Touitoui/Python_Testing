"""
Test suite for unknown email login bug fix.

Bug Description:
When a user tries to login with a non-existent email, the application would crash
because it attempted to access club[0] on an empty list.

Fix Description:
The /showSummary route now checks if the club list is empty before accessing it.
If no club is found, it returns to the index page instead of crashing.

Test Strategy:
- Test that non-existent emails don't crash the app
- Test that the user is redirected back to login page
- Test various invalid email formats
- Test boundary cases (empty strings, whitespace)
- Test that valid emails still work correctly
- Test that error handling doesn't affect valid logins
"""
import pytest


class TestUnknownEmailHandling:
    """Test that unknown emails are handled gracefully without crashing."""
    
    def test_nonexistent_email_does_not_crash(self, client, invalid_emails):
        """Test that logging in with non-existent email doesn't crash the app."""
        for email in invalid_emails:
            response = client.post('/showSummary', data={'email': email})
            # Should not raise an IndexError or crash
            assert response.status_code == 200
    
    def test_nonexistent_email_returns_to_login(self, client):
        """Test that non-existent email redirects back to index page."""
        response = client.post('/showSummary', data={'email': 'nonexistent@example.com'})
        assert response.status_code == 200
        # Check that we're back at the index/login page (contains email input)
        assert b'email' in response.data.lower()
    
    def test_empty_email_does_not_crash(self, client):
        """Test that empty email string doesn't crash the app."""
        response = client.post('/showSummary', data={'email': ''})
        assert response.status_code == 200
    
    def test_whitespace_email_does_not_crash(self, client):
        """Test that whitespace-only email doesn't crash the app."""
        response = client.post('/showSummary', data={'email': '   '})
        assert response.status_code == 200
    
    def test_malformed_emails_do_not_crash(self, client, malformed_emails):
        """Test that various malformed emails don't crash the app."""
        for email in malformed_emails:
            response = client.post('/showSummary', data={'email': email})
            assert response.status_code == 200
    
    def test_multiple_failed_logins_do_not_crash(self, client):
        """Test that multiple consecutive failed login attempts don't crash."""
        invalid_emails = [
            'first@fake.com',
            'second@fake.com',
            'third@fake.com'
        ]
        for email in invalid_emails:
            response = client.post('/showSummary', data={'email': email})
            assert response.status_code == 200


class TestValidEmail:
    """Test valid email login functionality."""
        
    def test_valid_email_shows_welcome_page(self, client, valid_club_email):
        """Test that valid login shows the welcome page with club data."""
        response = client.post('/showSummary', data={'email': valid_club_email})
        assert response.status_code == 200
        # Should not be the login page anymore
        response_text = response.data.decode('utf-8').lower()
        # Welcome page should have logout or points info
        assert 'points' in response_text or 'logout' in response_text
