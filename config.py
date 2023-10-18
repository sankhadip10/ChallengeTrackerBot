import os

BOT_TOKEN = os.environ.get('BOT_TOKEN')
sauce_option_un = os.environ.get('SAUCE_OPTION_UN')
sauce_option_access_key = os.environ.get('SAUCE_OPTION_ACCESS_KEY')

# config.py
BOT_COMMAND_ROLE = "BotCommander"

# Database Configurations (if you expand beyond SQLite)
DB_HOST = 'localhost'
DB_PORT = 5432  # example for PostgreSQL
DB_USER = 'username'
DB_PASS = 'password'
DB_NAME = 'database_name'

# Any other configuration constants you might need in the future
