"""Unit tests for 12 places maximum booking limit validation.

These tests ensure that clubs cannot book more than 12 places at a time,
verifying the fix for the bug where unlimited bookings were allowed.
"""
import pytest
from datetime import datetime, timedelta


class TestMaxPlacesLimitValidation:
    """Test suite for 12 places maximum booking restriction."""

    def test_cannot_book_13_places(self, client, sample_club, large_competition):
        """Test that booking 13 places (over limit) is rejected."""
        import server
        server.competitions.append(large_competition)
        
        initial_places = int(large_competition['numberOfPlaces'])
        
        # Attempt to book 13 places (exceeds max of 12)
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': large_competition['name'],
            'places': '13'
        }, follow_redirects=True)
        
        # Verify rejection
        assert response.status_code == 200
        assert b'You cannot book more than 12 places.' in response.data
        
        # Verify places were NOT decremented
        found_comp = [c for c in server.competitions if c['name'] == large_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places

    def test_can_book_12_places(self, client, sample_club, large_competition):
        """Test that booking exactly 12 places (at limit) succeeds."""
        import server
        server.competitions.append(large_competition)
        
        initial_places = int(large_competition['numberOfPlaces'])
        
        # Book exactly 12 places (maximum allowed)
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': large_competition['name'],
            'places': '12'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify places were decremented by 12
        found_comp = [c for c in server.competitions if c['name'] == large_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places - 12

    def test_can_book_11_places(self, client, sample_club, large_competition):
        """Test that booking 11 places (under limit) succeeds."""
        import server
        server.competitions.append(large_competition)
        
        initial_places = int(large_competition['numberOfPlaces'])
        
        # Book 11 places (under limit)
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': large_competition['name'],
            'places': '11'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify places were decremented by 11
        found_comp = [c for c in server.competitions if c['name'] == large_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places - 11
