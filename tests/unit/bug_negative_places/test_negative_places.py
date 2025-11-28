import pytest
from datetime import datetime, timedelta


class TestNegativePlacesValidation:
    """Test suite for preventing negative and zero place bookings."""

    def test_cannot_book_zero_places(self, client, sample_club, sample_competition):
        """Test that booking zero places is rejected."""
        import server
        server.competitions.append(sample_competition)
        
        initial_places = int(sample_competition['numberOfPlaces'])
        
        # Attempt to book zero places
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': sample_competition['name'],
            'places': '0'
        }, follow_redirects=True)
        
        # Verify rejection with appropriate message
        assert response.status_code == 200
        assert b'You must book at least one place.' in response.data
        
        # Verify places were NOT changed
        found_comp = [c for c in server.competitions if c['name'] == sample_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places

    def test_cannot_book_negative_one_place(self, client, sample_club, sample_competition):
        """Test that booking -1 places is rejected."""
        import server
        server.competitions.append(sample_competition)
        
        initial_places = int(sample_competition['numberOfPlaces'])
        
        # Attempt to book -1 places
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': sample_competition['name'],
            'places': '-1'
        }, follow_redirects=True)
        
        # Verify rejection
        assert response.status_code == 200
        assert b'You must book at least one place.' in response.data
        
        # Verify places were NOT incremented
        found_comp = [c for c in server.competitions if c['name'] == sample_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places

    def test_cannot_book_negative_several_place(self, client, sample_club, sample_competition):
        """Test that booking several negative numbers is rejected."""
        import server
        server.competitions.append(sample_competition)
        
        initial_places = int(sample_competition['numberOfPlaces'])
        
        # Attempt to book -100 places
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': sample_competition['name'],
            'places': '-100'
        }, follow_redirects=True)
        
        # Verify rejection
        assert response.status_code == 200
        assert b'You must book at least one place.' in response.data
        
        # Verify places were NOT changed
        found_comp = [c for c in server.competitions if c['name'] == sample_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places

    def test_can_book_one_place(self, client, sample_club, sample_competition):
        """Test that booking exactly 1 place succeeds (boundary case)."""
        import server
        server.competitions.append(sample_competition)
        
        initial_places = int(sample_competition['numberOfPlaces'])
        
        # Book 1 place (minimum valid amount)
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': sample_competition['name'],
            'places': '1'
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify places were decremented by 1
        found_comp = [c for c in server.competitions if c['name'] == sample_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places - 1

    def test_can_book_multiple_valid_places(self, client, sample_club, sample_competition):
        """Test that booking multiple valid places succeeds."""
        import server
        server.competitions.append(sample_competition)
        
        initial_places = int(sample_competition['numberOfPlaces'])
        places_to_book = 5
        
        # Book 5 places
        response = client.post('/purchasePlaces', data={
            'club': sample_club['name'],
            'competition': sample_competition['name'],
            'places': str(places_to_book)
        }, follow_redirects=True)
        
        # Verify success
        assert response.status_code == 200
        assert b'Great-booking complete!' in response.data
        
        # Verify places were correctly decremented
        found_comp = [c for c in server.competitions if c['name'] == sample_competition['name']][0]
        assert int(found_comp['numberOfPlaces']) == initial_places - places_to_book

