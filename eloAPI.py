import sqlite3
from flask import Flask, jsonify, request
from datetime import datetime


app = Flask(__name__)

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect('example.db')
    conn.row_factory = sqlite3.Row  # Allows row access by column name
    return conn

# Initialize database schema
with get_db_connection() as conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                league_name TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                team_1 TEXT NOT NULL,
                team_2 TEXT NOT NULL,
                score_team_1 INTEGER,
                score_team_2 INTEGER,
                winner_team TEXT
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS leagues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

@app.route('/api/games', methods=['POST'])
def add_game():
    data = request.get_json()
    league_name = data.get('league_name')
    timestamp = data.get('timestamp')
    team_1 = data.get('team_1')
    team_2 = data.get('team_2')
    score_team_1 = data.get('score_team_1')
    score_team_2 = data.get('score_team_2')
    
    if not all([league_name, timestamp, team_1, team_2, score_team_1, score_team_2]):
        return jsonify(error="Missing required fields"), 400

    if score_team_1 > score_team_2:
        winner_team = team_1
    elif score_team_2 > score_team_1:
        winner_team = team_2
    else:
        winner_team = "Draw"

    with get_db_connection() as conn:
        conn.execute('INSERT OR IGNORE INTO leagues (name) VALUES (?)', (league_name,))
        
        conn.execute('''
            INSERT INTO games (league_name, timestamp, team_1, team_2, score_team_1, score_team_2, winner_team)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (league_name, timestamp, team_1, team_2, score_team_1, score_team_2, winner_team))
        
        conn.commit()

    return jsonify(message="Game added successfully"), 201


if __name__ == '__main__':
    app.run(debug=True)

    