"""Unit tests for points validation before booking.

These tests ensure that clubs cannot book more places than they have points for,
verifying the fix for the bug where clubs could overspend their points.
"""
import pytest
from datetime import datetime, timedelta


class TestPointsValidation:
    """Test suite for preventing clubs from using more points than they own."""

    def test_cannot_book_more_places_than_points_available(self, client, club_with_10_points, standard_competition):
        """Test that booking more places than available points is rejected."""
        import server
        server.clubs.append(club_with_10_points)
        server.competitions.append(standard_competition)
        
        # Try to book 11 places when only 10 points available
        response = client.post('/purchasePlaces', data={
            'club': club_with_10_points['name'],
            'competition': standard_competition['name'],
            'places': '11'
        }, follow_redirects=True)
        
        # Verify rejection
        assert response.status_code == 200
        assert b'You do not have enough points to book this many places.' in response.data
        
        # Verify points were NOT decremented
        found_club = [c for c in server.clubs if c['name'] == club_with_10_points['name']][0]
        assert int(found_club['points']) == 10

    def test_can_book_exactly_all_points(self, client, club_with_10_points, standard_competition):
        """Test that booking exactly as many places as points succeeds."""
        import server
        server.clubs.append(club_with_10_points)
        server.competitions.append(standard_competition)
        
        # Book 10 places with 10 points
        response = client.post('/purchasePlaces', data={
            'club': club_with_10_points['name'],
            'competition': standard_competition['name'],
            'places': '10'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify competition places decremented
        found_comp = [c for c in server.competitions if c['name'] == standard_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == 15

    def test_can_book_less_than_available_points(self, client, club_with_10_points, standard_competition):
        """Test that booking fewer places than available points succeeds."""
        import server
        server.clubs.append(club_with_10_points)
        server.competitions.append(standard_competition)
        
        # Book 3 places when 10 points available
        response = client.post('/purchasePlaces', data={
            'club': club_with_10_points['name'],
            'competition': standard_competition['name'],
            'places': '3'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data

    def test_cannot_book_with_zero_points(self, client, club_with_0_points, standard_competition):
        """Test that a club with 0 points cannot book any places."""
        import server
        server.clubs.append(club_with_0_points)
        server.competitions.append(standard_competition)
        
        # Try to book 1 place with 0 points
        response = client.post('/purchasePlaces', data={
            'club': club_with_0_points['name'],
            'competition': standard_competition['name'],
            'places': '1'
        }, follow_redirects=True)
        
        # Verify rejection
        assert b'You do not have enough points to book this many places.' in response.data

    def test_cannot_book_one_more_than_points(self, client, club_with_10_points, standard_competition):
        """Test edge case: trying to book just one more place than points available."""
        import server
        server.clubs.append(club_with_10_points)
        server.competitions.append(standard_competition)
        
        # Try to book 11 places when 10 points available
        response = client.post('/purchasePlaces', data={
            'club': club_with_10_points['name'],
            'competition': standard_competition['name'],
            'places': '11'
        }, follow_redirects=True)
        
        # Verify rejection
        assert b'You do not have enough points to book this many places.' in response.data
