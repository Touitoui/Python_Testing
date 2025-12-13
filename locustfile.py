"""
Locust performance test file for GUDLFT booking platform.

Usage:
    1. Start your Flask app:
       flask run
    
    2. In another terminal, run Locust:
       locust
    
    3. Open browser to http://localhost:8089
    
    4. Configure:
       - Number of users (peak users to simulate)
       - Spawn rate (users added per second)
       - Host: http://127.0.0.1:5000
    
    5. Click "Start swarming" to begin tests

Command line options:
    locust --headless --users 10 --spawn-rate 2 --run-time 1m --host http://127.0.0.1:5000
"""
from locust import HttpUser, task, between
import json


class GUDLFTUser(HttpUser):
    """
    Simulates a user interacting with the GUDLFT booking platform.
    
    wait_time: Time between consecutive tasks (1-3 seconds)
    """
    wait_time = between(1, 3)
    
    def on_start(self):
        """
        Called when a simulated user starts.
        Load test data from JSON files.
        """
        with open('clubs.json') as f:
            self.clubs = json.load(f)['clubs']
        
        with open('competitions.json') as f:
            self.competitions = json.load(f)['competitions']
    
    @task(3)
    def view_homepage(self):
        """
        Task: View the homepage.
        Weight: 3 (executed 3x more often than other tasks)
        """
        self.client.get("/")
    
    @task(2)
    def view_points_display(self):
        """
        Task: View the public points display page.
        Weight: 2 (executed 2x more often than booking tasks)
        """
        self.client.get("/pointDisplay")
    
    @task(1)
    def login_and_view_summary(self):
        """
        Task: Login with valid email and view summary.
        Weight: 1 (baseline frequency)
        """
        if self.clubs:
            club = self.clubs[0]  # Use first club
            response = self.client.post("/showSummary", data={
                "email": club['email']
            })
            
            # Verify successful login
            if response.status_code != 200:
                response.failure(f"Login failed with status {response.status_code}")
    
    @task(1)
    def attempt_booking(self):
        """
        Task: Attempt to book places for a competition.
        Weight: 1 (baseline frequency)
        
        This simulates the full booking flow:
        1. Login
        2. Navigate to booking page
        3. Submit booking
        """
        if self.clubs and self.competitions:
            club = self.clubs[0]
            competition = self.competitions[0]
            
            # First, login
            login_response = self.client.post("/showSummary", data={
                "email": club['email']
            })
            
            if login_response.status_code == 200:
                # Then attempt booking
                booking_response = self.client.post("/purchasePlaces", data={
                    "club": club['name'],
                    "competition": competition['name'],
                    "places": "1"  # Book 1 place
                })
                
                if booking_response.status_code != 200:
                    booking_response.failure(f"Booking failed with status {booking_response.status_code}")
    
    @task(1)
    def view_booking_page(self):
        """
        Task: View a competition booking page.
        Weight: 1 (baseline frequency)
        """
        if self.clubs and self.competitions:
            club = self.clubs[0]
            competition = self.competitions[0]
            
            self.client.get(f"/book/{competition['name']}/{club['name']}")


class AdminUser(HttpUser):
    """
    Simulates an admin/power user who primarily views points.
    Lighter weight class for monitoring-focused users.
    """
    wait_time = between(2, 5)
    
    @task(5)
    def view_points_display(self):
        """View points display frequently."""
        self.client.get("/pointDisplay")
    
    @task(1)
    def view_homepage(self):
        """Occasionally view homepage."""
        self.client.get("/")


class AnonymousUser(HttpUser):
    """
    Simulates anonymous visitors who only view public pages.
    """
    wait_time = between(1, 4)
    
    @task(3)
    def view_homepage(self):
        """View homepage."""
        self.client.get("/")
    
    @task(2)
    def view_points_display(self):
        """View public points display."""
        self.client.get("/pointDisplay")
    
    @task(1)
    def attempt_invalid_login(self):
        """Try login with invalid email."""
        self.client.post("/showSummary", data={
            "email": "invalid@email.com"
        })
