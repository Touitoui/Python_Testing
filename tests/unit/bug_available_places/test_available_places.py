"""Unit tests for available places validation.

These tests ensure that clubs cannot book more places than are available
in a competition, verifying the fix for the overbooking bug.
"""
import pytest
from datetime import datetime, timedelta


class TestAvailablePlacesValidation:
    """Test suite for preventing overbooking of competitions."""

    def test_cannot_book_more_than_available(self, client, sample_club, competition_with_5_places):
        """Test that booking more places than available is rejected."""
        import server
        server.competitions.append(competition_with_5_places)
        
        # Try to book 6 places when only 5 are available
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': competition_with_5_places['name'],
            'places': '6'
        }, follow_redirects=True)
        
        # Verify rejection
        assert response.status_code == 200
        assert b'Not enough places available in this competition.' in response.data
        
        # Verify places were NOT decremented
        found_comp = [c for c in server.competitions if c['name'] == competition_with_5_places['name']][0]
        assert int(found_comp['numberOfPlaces']) == 5

    def test_can_book_exactly_all_available_places(self, client, sample_club, competition_with_5_places):
        """Test that booking exactly all available places succeeds."""
        import server
        server.competitions.append(competition_with_5_places)
        
        # Book all 5 available places
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': competition_with_5_places['name'],
            'places': '5'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify places are now 0
        found_comp = [c for c in server.competitions if c['name'] == competition_with_5_places['name']][0]
        assert int(found_comp['numberOfPlaces']) == 0

    def test_can_book_less_than_available(self, client, sample_club, competition_with_5_places):
        """Test that booking fewer places than available succeeds."""
        import server
        server.competitions.append(competition_with_5_places)
        
        # Book 3 places when 5 are available
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': competition_with_5_places['name'],
            'places': '3'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify places decremented correctly
        found_comp = [c for c in server.competitions if c['name'] == competition_with_5_places['name']][0]
        assert int(found_comp['numberOfPlaces']) == 2

    def test_cannot_book_when_competition_has_one_place_and_request_two(self, client, sample_club, competition_with_1_place):
        """Test overbooking rejection when only 1 place available."""
        import server
        server.competitions.append(competition_with_1_place)
        
        # Try to book 2 places when only 1 is available
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': competition_with_1_place['name'],
            'places': '2'
        }, follow_redirects=True)
        
        # Verify rejection
        assert response.status_code == 200
        assert b'Not enough places available in this competition.' in response.data
        
        # Verify the 1 place is still available
        found_comp = [c for c in server.competitions if c['name'] == competition_with_1_place['name']][0]
        assert int(found_comp['numberOfPlaces']) == 1

    def test_can_book_last_place(self, client, sample_club, competition_with_1_place):
        """Test that booking the last available place succeeds."""
        import server
        server.competitions.append(competition_with_1_place)
        
        # Book the last place
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': competition_with_1_place['name'],
            'places': '1'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify competition is now full
        found_comp = [c for c in server.competitions if c['name'] == competition_with_1_place['name']][0]
        assert int(found_comp['numberOfPlaces']) == 0
