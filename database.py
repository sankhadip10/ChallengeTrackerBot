import sqlite3

# Connection to the SQLite database
conn = sqlite3.connect('events.db')
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
        end_date TEXT
    )
    ''')

    # User table setup
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        is_registered INTEGER NOT NULL
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

    conn.commit()


# Event-related functions
def add_event(event_name, duration, start_date, end_date):
    """Add a new event to the database."""
    try:
        print("Attempting to add event to the database...")
        cursor.execute("INSERT INTO events (event_name, duration, start_date, end_date) VALUES (?, ?, ?, ?)",
                       (event_name, duration, start_date, end_date))
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
        event_name, duration, start_date, end_date = event
        events_dict[event_name] = {
            'duration': duration,
            'start_date': start_date,
            'end_date': end_date
        }
    return events_dict


# Registration and posts-related functions
def is_user_registered(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone() is not None


def register_user(user_id):
    if not is_user_registered(user_id):  # check if the user is already registered
        cursor.execute("INSERT INTO users (user_id, is_registered) VALUES (?, 1)", (user_id,))
        conn.commit()
        print(f"User {user_id} registered successfully.")
    else:
        print(f"User {user_id} is already registered.")


def add_daily_post(user_id, url):
    import datetime
    current_date = datetime.datetime.now().date().isoformat()
    cursor.execute("INSERT INTO posts (user_id, post_date, post_url) VALUES (?, ?, ?)", (user_id, current_date, url))
    conn.commit()


# Initialize tables when the module is imported
setup()

