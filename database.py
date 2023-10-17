import sqlite3
from datetime import datetime
from datetime import datetime, date
import os

# Determine the database path based on the environment
DB_PATH = 'test_events.db' if os.environ.get('TEST_ENV') else 'events.db'

# Connection to the SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# Table creation
def setup():
    """Set up the necessary tables."""

    # Event table setup
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_name TEXT PRIMARY KEY,
        duration INTEGER,
        start_date TEXT,
        end_date TEXT,
        token_reward INTEGER
    )
    ''')

    # User table setup
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER,
        event_name TEXT,
        is_registered INTEGER NOT NULL,
        PRIMARY KEY (user_id, event_name),
        FOREIGN KEY (event_name) REFERENCES events(event_name)
    )
    ''')

    # Posts table setup
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        user_id INTEGER,
        post_date TEXT NOT NULL,
        post_url TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
    ''')

    # Create a  Table for User Balances
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_balances (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
    );

    ''')

    # User event streak table setup
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_event_streaks (
        user_id INTEGER,
        event_name TEXT,
        streak INTEGER DEFAULT 0,
        last_post_date TEXT,
        is_eligible INTEGER DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (event_name) REFERENCES events(event_name)
    )
    ''')



    conn.commit()


# Event-related functions
def add_event(event_name, duration, start_date, end_date, token_reward):
    """Add a new event to the database."""
    try:
        print("Attempting to add event to the database...")
        cursor.execute("INSERT INTO events (event_name, duration, start_date, end_date, token_reward) VALUES (?, ?, ?, ?, ?)",
                       (event_name, duration, start_date, end_date, token_reward))
        conn.commit()
        print("Event added successfully.")

    except sqlite3.IntegrityError:
        print(f"Event with the name {event_name} already exists in the database!")

    except sqlite3.ProgrammingError as pe:
        print(f"A programming error occurred: {pe}")

    except sqlite3.OperationalError as oe:
        print(f"An operational error occurred: {oe}")

    except Exception as e:
        # Generic error handling
        print(f"An unexpected error occurred: {e}")



def delete_event(event_name):
    """Remove an event from the database."""
    cursor.execute("DELETE FROM events WHERE event_name=?", (event_name,))
    conn.commit()


def get_all_events():
    """Retrieve all events from the database."""
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    events_dict = {}
    for event in events:
        event_name, duration, start_date, end_date, token_reward = event
        events_dict[event_name] = {
            'duration': duration,
            'start_date': start_date,
            'end_date': end_date,
            'token_reward': token_reward
        }
    return events_dict



# Registration and posts-related functions
def is_user_registered(user_id, event_name):
    cursor.execute("SELECT * FROM users WHERE user_id=? AND event_name=?", (user_id, event_name))
    return cursor.fetchone() is not None


def register_user(user_id, event_name):
    if not is_user_registered(user_id, event_name):  # check if the user is already registered for the event
        cursor.execute("INSERT INTO users (user_id, event_name, is_registered) VALUES (?, ?, 1)", (user_id, event_name))
        conn.commit()
        print(f"User {user_id} registered successfully for event {event_name}.")
    else:
        print(f"User {user_id} is already registered for event {event_name}.")

def get_all_users():
    """Retrieve all registered users from the database."""
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    # Flatten the list of tuples to a single list
    user_ids = [user[0] for user in users]

    return user_ids



def add_daily_post(user_id, url):
    current_date = datetime.now().date().isoformat()
    cursor.execute("INSERT INTO posts (user_id, post_date, post_url) VALUES (?, ?, ?)", (user_id, current_date, url))
    conn.commit()

# Function to update or reset the streak
def update_streak(user_id, event_name, date_posted):
    cursor.execute(
        "SELECT streak, last_post_date, is_eligible FROM user_event_streaks WHERE user_id=? AND event_name=?",
        (user_id, event_name))
    result = cursor.fetchone()

    # Fetch the event's duration from the events table
    cursor.execute("SELECT duration FROM events WHERE event_name=?", (event_name,))
    event_duration = cursor.fetchone()[0]

    # If the user hasn't posted for this event before
    if not result:
        cursor.execute(
            "INSERT INTO user_event_streaks (user_id, event_name, streak, last_post_date, is_eligible) VALUES (?, ?, 1, ?, 1)",
            (user_id, event_name, date_posted))
    else:
        streak, last_post_date, is_eligible = result

        # If user's last post was yesterday
        if (date_posted - datetime.strptime(last_post_date, '%Y-%m-%d').date()).days == 1:
            streak += 1
        else:
            streak = 1
            is_eligible = 0

        # Check if streak matches the event's duration
        if streak == event_duration:
            is_eligible = 1
        else:
            is_eligible = 0

        cursor.execute(
            "UPDATE user_event_streaks SET streak=?, last_post_date=?, is_eligible=? WHERE user_id=? AND event_name=?",
            (streak, date_posted, is_eligible, user_id, event_name))

    conn.commit()


def get_user_streak(user_id, event_name):
    cursor.execute("SELECT streak FROM user_event_streaks WHERE user_id=? AND event_name=?", (user_id, event_name))
    result = cursor.fetchone()
    if result:
        return result[0]
    return 0


def get_eligible_users(event_name):
    # Retrieve event's duration
    cursor.execute("SELECT duration FROM events WHERE event_name=?", (event_name,))
    result = cursor.fetchone()

    # If no event with the given name exists, return an empty list
    if result is None:
        print(f"No event found with name: {event_name}")
        return []

    event_duration = result[0]

    cursor.execute("""
        SELECT user_id, streak, last_post_date 
        FROM user_event_streaks 
        WHERE event_name=? AND streak=?
    """, (event_name, event_duration))

    eligible_users = [{"user_id": user[0], "streak": user[1], "last_post_date": user[2]} for user in cursor.fetchall()]
    return eligible_users

def distribute_tokens(event_name):
    # Fetch the token amount for the event
    cursor.execute("SELECT token_reward FROM events WHERE event_name=?", (event_name,))
    token_amount = cursor.fetchone()[0]

    # Fetch eligible users
    eligible_users = get_eligible_users(event_name)

    # Distribute tokens to eligible users
    for user in eligible_users:
        user_id = user["user_id"]
        cursor.execute("INSERT INTO user_balances (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?", (user_id, token_amount, token_amount))

    conn.commit()


def has_posted_today(user_id, event_name, current_date):
    """Check if the user has already posted for the given event on the current date."""
    cursor.execute("SELECT * FROM posts WHERE user_id=? AND post_date=?", (user_id, current_date.isoformat()))
    return cursor.fetchone() is not None



# Initialize tables when the module is imported
setup()
