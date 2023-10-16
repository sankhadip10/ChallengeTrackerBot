# import unittest
# from unittest.mock import Mock, patch
# import sqlite3
# # from events_feature import createEvent  # Import your command
#
# class TestBotCommands(unittest.TestCase):
#
#     def setUp(self):
#         # Set up an in-memory database
#         self.conn = sqlite3.connect(':memory:')
#         self.cursor = self.conn.cursor()
#
#         # Set up your tables here. I'll just set up 'events' as an example.
#         self.cursor.execute('''
#             CREATE TABLE IF NOT EXISTS events
#             (event_name TEXT, duration INTEGER, start_date TEXT, end_date TEXT)
#         ''')
#
#         # Mock the command's context
#         self.ctx = Mock()
#         self.ctx.send = Mock()
#
#     def test_create_event(self):
#         # Call your command function
#         createEvent(self.ctx, "TestEvent", 5, "10-10-2023", "15-10-2023")
#
#         # Check that the event was added to the database
#         self.cursor.execute("SELECT event_name FROM events WHERE event_name=?", ("TestEvent",))
#         result = self.cursor.fetchone()
#
#         self.assertIsNotNone(result)
#         self.assertEqual(result[0], "TestEvent")
#
#         # Check that a success message was sent
#         self.ctx.send.assert_called_with("Event TestEvent created successfully!")
#
#     def tearDown(self):
#         self.conn.close()
#
# if __name__ == "__main__":
#     unittest.main()
