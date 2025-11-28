"""Unit tests for time-based booking validation.

These tests ensure that users cannot book places for past competitions,
verifying the fix for the bug where past competition bookings were allowed.
"""
import pytest
from datetime import datetime, timedelta


class TestBookingTimeValidation:
    """Test suite for competition booking time restrictions."""

    def test_cannot_book_past_competition(self, client, sample_club, past_competition):
        """Test that booking a past competition is rejected."""
        # Add past competition to the competitions list
        import server
        server.competitions.append(past_competition)
        
        # Attempt to book places for past competition
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': past_competition['name'],
            'places': '5'
        }, follow_redirects=True)
        
        # Verify response contains error message
        assert response.status_code == 200
        assert b'Cannot book places for past competitions.' in response.data
        
        # Verify places were NOT decremented
        found_comp = [c for c in server.competitions if c['name'] == past_competition['name']][0]
        assert found_comp['numberOfPlaces'] == past_competition['numberOfPlaces']

    def test_can_book_future_competition(self, client, sample_club, future_competition):
        """Test that booking a future competition succeeds."""
        import server
        server.competitions.append(future_competition)
        
        initial_places = int(future_competition['numberOfPlaces'])
        places_to_book = 3
        
        # Book places for future competition
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': future_competition['name'],
            'places': str(places_to_book)
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify places were decremented
        found_comp = [c for c in server.competitions if c['name'] == future_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places - places_to_book

    def test_cannot_book_competition_at_exact_current_time(self, client, sample_club, today_competition):
        """Test that booking a competition at exactly current time is rejected (edge case)."""
        import server
        server.competitions.append(today_competition)
        
        # Attempt to book - should fail because date <= now
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': today_competition['name'],
            'places': '2'
        }, follow_redirects=True)
        
        # Should be rejected (using <= comparison)
        assert response.status_code == 200
        assert b'Cannot book places for past competitions.' in response.data

    def test_past_competition_one_second_ago(self, client, sample_club):
        """Test that a competition 1 second in the past is rejected."""
        import server
        
        # Create competition just 1 second ago
        past_by_second = (datetime.now() - timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
        competition = {
            "name": "Just Past Competition",
            "date": past_by_second,
            "numberOfPlaces": "10"
        }
        server.competitions.append(competition)
        
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': competition['name'],
            'places': '1'
        }, follow_redirects=True)
        
        assert b'Cannot book places for past competitions.' in response.data

    def test_future_competition_one_second_ahead(self, client, sample_club):
        """Test that a competition 1 second in the future is allowed."""
        import server
        
        # Create competition just 1 second ahead
        future_by_second = (datetime.now() + timedelta(seconds=1)).strftime("%Y-%m-%d %H:%M:%S")
        competition = {
            "name": "Just Future Competition",
            "date": future_by_second,
            "numberOfPlaces": "10"
        }
        server.competitions.append(competition)
        
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': competition['name'],
            'places': '1'
        }, follow_redirects=True)
        
        assert b'Great-booking complete!' in response.data

    def test_existing_past_competitions_in_json(self, client, sample_club):
        """Test that existing competitions in competitions.json with past dates are rejected.
        
        Note: competitions.json contains competitions from 2020, which are in the past.
        """
        import server
        
        # Get competitions from the actual JSON file - they're all from 2020
        past_comps = [c for c in server.competitions if c['date'] < datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        
        if past_comps:
            past_comp = past_comps[0]
            response = client.post('/purchasePlaces', data={
                'club': sample_club['name'],
                'competition': past_comp['name'],
                'places': '1'
            }, follow_redirects=True)
            
            assert b'Cannot book places for past competitions.' in response.data
