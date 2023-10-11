import sqlite3

# Connection to the SQLite database (this will create a file called events.db in the local directory)
conn = sqlite3.connect('events.db')
cursor = conn.cursor()

def setup():
    """Create the table if it doesn't exist."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        event_name TEXT PRIMARY KEY,
        duration INTEGER,
        start_date TEXT,
        end_date TEXT
    )
    ''')
    conn.commit()

def add_event(event_name, duration):
    """Add a new event to the database."""
    # Here, we are using placeholders to prevent SQL injection
    cursor.execute("INSERT INTO events (event_name, duration, start_date, end_date) VALUES (?, ?, ?, ?)",
                   (event_name, duration, "Start Date Placeholder", "End Date Placeholder"))
    conn.commit()

def delete_event(event_name):
    """Remove an event from the database."""
    cursor.execute("DELETE FROM events WHERE event_name=?", (event_name,))
    conn.commit()

def get_all_events():
    """Retrieve all events from the database."""
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    # Convert the list of tuples to a dictionary for easier processing
    events_dict = {}
    for event in events:
        event_name, duration, start_date, end_date = event
        events_dict[event_name] = {
            'duration': duration,
            'start_date': start_date,
            'end_date': end_date
        }

    return events_dict

# Set up the database table when the module is imported
setup()
