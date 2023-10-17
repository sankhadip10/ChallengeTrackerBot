import os
# Set the environment variable to use the test database
os.environ['TEST_ENV'] = '1'
import pytest
import sqlite3
import json
import database as db
from datetime import datetime, date



# Load mock data from fixtures
with open('tests/fixtures/events.json', 'r') as f:
    mock_events = json.load(f)

with open('tests/fixtures/users.json', 'r') as f:
    mock_users = json.load(f)

# Setup function to populate the test database with mock data
def setup_module():
    for event in mock_events:
        db.add_event(**event)
    for user in mock_users:
        db.register_user(user['user_id'])

# Teardown function to clear the test database
def teardown_module():
    conn = sqlite3.connect('test_events.db')
    cursor = conn.cursor()

    # Check if the 'events' table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
    if cursor.fetchone():
        cursor.execute("DELETE FROM events")
    conn.commit()
    conn.close()


def test_add_event():
    # Test adding a new event
    event = {
        "event_name": "NewTestEvent",
        "duration": 7,
        "start_date": "10-01-2023",
        "end_date": "16-01-2023",
        "token_reward": 15
    }
    db.add_event(**event)
    events = db.get_all_events()
    assert "NewTestEvent" in events

def test_get_all_events():
    events = db.get_all_events()
    assert "TestEvent1" in events, "TestEvent1 should be in the list of events"


def test_add_daily_post():
    user_id = mock_users[0]['user_id']
    url = "http://testurl.com"
    db.add_daily_post(user_id, url)

    # Check if the post was added
    cursor = db.conn.cursor()
    cursor.execute("SELECT post_url FROM posts WHERE user_id=?", (user_id,))
    post_url = cursor.fetchone()[0]
    assert post_url == url, f"Expected post URL {url}, but got {post_url}"


def test_update_streak():
    user_id = mock_users[0]['user_id']
    event_name = "TestEvent1"
    date_posted = datetime.now().date()
    db.update_streak(user_id, event_name, date_posted)

    streak = db.get_user_streak(user_id, event_name)
    assert streak == 1, f"Expected streak of 1 for user {user_id}, but got {streak}"
