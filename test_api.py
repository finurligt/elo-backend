import unittest
import json
from eloAPI import app, get_db_connection  # Import your Flask app and DB connection function

class APITestCase(unittest.TestCase):
    def setUp(self):
        # Configure Flask app to use testing mode and in-memory SQLite database
        app.config['TESTING'] = True
        app.config['DATABASE'] = ':memory:'
        self.client = app.test_client()
        
        # Initialize the in-memory database with the schema
        with app.app_context():
            conn = get_db_connection()
            conn.execute('''CREATE TABLE IF NOT EXISTS games (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                league_name TEXT NOT NULL,
                                timestamp DATETIME NOT NULL,
                                team_1 TEXT NOT NULL,
                                team_2 TEXT NOT NULL,
                                score_team_1 INTEGER,
                                score_team_2 INTEGER,
                                winner_team TEXT)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS leagues (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT UNIQUE NOT NULL)''')
            conn.commit()

    def test_add_game_success(self):
        # Prepare mock data for a successful request
        game_data = {
            "league_name": "Football League",
            "timestamp": "2023-11-07 15:00:00",
            "team_1": "Team A",
            "team_2": "Team B",
            "score_team_1": 3,
            "score_team_2": 1
        }
        response = self.client.post('/api/games', data=json.dumps(game_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn("Game added successfully", response.get_data(as_text=True))

    def test_add_game_missing_field(self):
        # Missing required field `team_2`
        game_data = {
            "league_name": "Football League",
            "timestamp": "2023-11-07 15:00:00",
            "team_1": "Team A",
            "score_team_1": 3,
            "score_team_2": 1
        }
        response = self.client.post('/api/games', data=json.dumps(game_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Missing required fields", response.get_data(as_text=True))

    def tearDown(self):
        # Clean up and close the database after each test
        with app.app_context():
            conn = get_db_connection()
            conn.execute('DROP TABLE IF EXISTS games')
            conn.execute('DROP TABLE IF EXISTS leagues')
            conn.commit()

if __name__ == '__main__':
    unittest.main()
