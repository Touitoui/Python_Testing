"""Unit tests for club points deduction after booking.

These tests ensure that club points are correctly deducted when booking places,
verifying the fix for the bug where points weren't properly updated.
"""
import pytest
from datetime import datetime, timedelta


class TestPointsDeduction:
    """Test suite for verifying points are deducted after booking."""

    def test_points_deducted_after_booking(self, client, standard_club, standard_competition):
        """Test that club points are deducted by the number of places booked."""
        import server
        server.clubs.append(standard_club)
        server.competitions.append(standard_competition)
        
        initial_points = int(standard_club['points'])
        places_to_book = 3
        
        # Book 3 places
        response = client.post('/purchasePlaces', data={
            'club': standard_club['name'],
            'competition': standard_competition['name'],
            'places': str(places_to_book)
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify points were deducted
        found_club = [c for c in server.clubs if c['name'] == standard_club['name']][0]
        assert int(found_club['points']) == initial_points - places_to_book

    def test_points_deducted_for_single_place(self, client, standard_club, standard_competition):
        """Test that points are deducted correctly for a single place booking."""
        import server
        server.clubs.append(standard_club)
        server.competitions.append(standard_competition)
        
        initial_points = int(standard_club['points'])
        
        # Book 1 place
        response = client.post('/purchasePlaces', data={
            'club': standard_club['name'],
            'competition': standard_competition['name'],
            'places': '1'
        }, follow_redirects=True)
        
        assert b'Great-booking complete!' in response.data
        
        # Verify 1 point was deducted
        found_club = [c for c in server.clubs if c['name'] == standard_club['name']][0]
        assert int(found_club['points']) == initial_points - 1

    def test_points_deducted_for_multiple_places(self, client, standard_club, standard_competition):
        """Test that points are deducted correctly for multiple places."""
        import server
        server.clubs.append(standard_club)
        server.competitions.append(standard_competition)
        
        initial_points = int(standard_club['points'])
        places_to_book = 7
        
        # Book 7 places
        response = client.post('/purchasePlaces', data={
            'club': standard_club['name'],
            'competition': standard_competition['name'],
            'places': str(places_to_book)
        }, follow_redirects=True)
        
        assert b'Great-booking complete!' in response.data
        
        # Verify 7 points were deducted
        found_club = [c for c in server.clubs if c['name'] == standard_club['name']][0]
        assert int(found_club['points']) == initial_points - places_to_book
