import database as db

# Test adding a new event
print("Attempting to add event to the database...")
db.add_event("Test Event", 10, "2021-01-01", "2021-01-10")
print("Event added successfully.")

# List all events
print("\nAll events:")
events = db.get_all_events()
for name, details in events.items():
    print(name, details)

# Test registration functionality
user_id = 1234567890  # Test user ID
print(f"\nIs user {user_id} registered?", db.is_user_registered(user_id))
print(f"Registering user {user_id}...")
db.register_user(user_id)
print(f"Is user {user_id} registered?", db.is_user_registered(user_id))

# List all registered users
print("\nAll registered users:")
users = db.get_all_users()
for user_id in users:
    print(user_id)


# Test adding a daily post
print(f"\nAdding a daily post for user {user_id}...")
db.add_daily_post(user_id, "http://example.com/post1")

# To retrieve and verify the daily post, you'll need to manually check the database for now
# In the future, you can also add a function in `database.py` to retrieve posts for a given user

print("\nTests complete!")
