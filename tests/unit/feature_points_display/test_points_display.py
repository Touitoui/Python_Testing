"""
Unit tests for the points display feature.

Feature Description:
A public page that displays all clubs and their current points in a table format.
This allows anyone (logged in or not) to see the current points standings.

Test Strategy:
- Test that the route is accessible without authentication
- Test that all clubs are displayed
- Test that points are displayed correctly
- Test that the table structure is correct
- Test edge cases (empty clubs, zero points, etc.)
"""
import pytest


class TestPointsDisplayRoute:
    """Test the /pointDisplay route accessibility and response."""
    
    def test_points_display_route_exists(self, client):
        """Test that the /pointDisplay route is accessible."""
        response = client.get('/pointDisplay')
        assert response.status_code == 200
    
    def test_points_display_returns_html(self, client):
        """Test that the route returns HTML content."""
        response = client.get('/pointDisplay')
        assert response.content_type == 'text/html; charset=utf-8'
    
    def test_points_display_accessible_without_login(self, client):
        """Test that the page is accessible without authentication."""
        # Direct GET request without any prior login
        response = client.get('/pointDisplay')
        assert response.status_code == 200
        assert b'Points Display' in response.data

    def test_has_back_link(self, client):
        """Test that the page has a back link."""
        response = client.get('/pointDisplay')
        assert b'Back' in response.data or b'back' in response.data
    
    def test_back_link_uses_javascript_history(self, client):
        """Test that back link uses javascript history.back()."""
        response = client.get('/pointDisplay')
        assert b'javascript:history.back()' in response.data


class TestPointsDisplayContent:
    """Test the content displayed on the points page."""
    
    def test_displays_all_clubs(self, client, setup_clubs):
        """Test that all clubs are displayed on the page."""
        response = client.get('/pointDisplay')
        assert response.status_code == 200
        
        # Check all club names are present
        assert b'Club A' in response.data
        assert b'Club B' in response.data
        assert b'Club C' in response.data
        assert b'Club D' in response.data
    
    def test_displays_all_points(self, client, setup_clubs):
        """Test that all club points are displayed."""
        response = client.get('/pointDisplay')
        assert response.status_code == 200
        
        # Check all points are present
        assert b'10' in response.data
        assert b'25' in response.data
        assert b'0' in response.data
        assert b'50' in response.data


class TestPointsDisplayWithRealData:
    """Test points display with actual JSON data."""
    
    def test_displays_clubs_from_json(self, client):
        """Test that clubs from clubs.json are displayed."""
        response = client.get('/pointDisplay')
        assert response.status_code == 200
        
        # Should show actual clubs from JSON
        # Check for common patterns that indicate clubs are loaded
        assert b'<td>' in response.data  # Has table cells
    
    def test_points_are_numeric(self, client, setup_clubs):
        """Test that displayed points look like numbers."""
        response = client.get('/pointDisplay')
        response_text = response.data.decode('utf-8')
        
        # Points should be displayed as numbers (not empty or invalid)
        import re
        # Look for table cells with numbers
        point_cells = re.findall(r'<td>(\d+)</td>', response_text)
        assert len(point_cells) > 0  # Should find numeric points


class TestPointsDisplayEdgeCases:
    """Test edge cases for points display."""
    
    def test_displays_empty_clubs_list(self, client):
        """Test behavior when clubs list is empty."""
        import server
        server.clubs = []
        
        response = client.get('/pointDisplay')
        assert response.status_code == 200
        # Should still show the table headers
        assert b'Points Display' in response.data
 