import tempfile
import os
import pytest
import discord
from unittest.mock import Mock
from unittest.mock import AsyncMock
from events_feature import EventsCog
from unittest.mock import patch
from discord.ext import commands
@pytest.mark.asyncio
async def test_createEvent_short_name():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Call the createEvent command with a short event name
    await cog.createEvent.callback(cog, ctx=ctx, eventName="Ev", duration=5, start_date="01-01-2023",
                                   end_date="05-01-2023", token_reward=10)

    # Check that the bot sent the expected response
    ctx.send.assert_called_once_with("Event name should be between 3 and 50 characters long.")
@pytest.mark.asyncio
async def test_createEvent_invalid_characters():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Call the createEvent command with an event name containing invalid characters
    await cog.createEvent.callback(cog,ctx=ctx, eventName="Event@123", duration=5, start_date="01-01-2023", end_date="05-01-2023", token_reward=10)

    # Check that the bot sent the expected response
    ctx.send.assert_called_once_with("Event name contains invalid characters. Only alphanumeric characters, hyphens, and underscores are allowed.")

@pytest.mark.asyncio
async def test_createEvent_invalid_date_format():
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    cog = EventsCog(bot)

    await cog.createEvent.callback(cog, ctx=ctx, eventName="ValidEvent", duration=5, start_date="01/01/2023", end_date="05/01/2023", token_reward=10)

    ctx.send.assert_called_once_with("The date format is incorrect! Please use DD-Month-YYYY format (e.g., 15-10-2023).")

@pytest.mark.asyncio
async def test_createEvent_mismatched_duration():
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    cog = EventsCog(bot)

    await cog.createEvent.callback(cog, ctx=ctx, eventName="ValidEvent", duration=7, start_date="01-01-2023", end_date="05-01-2023", token_reward=10)

    ctx.send.assert_called_once_with(
        f"The provided duration doesn't match the start and end dates. It should be 7 days,instead its giving difference 5 days.")


@pytest.mark.asyncio
@patch('events_feature.db.get_all_events', return_value={"ExistingEvent": {}})
async def test_createEvent_event_already_exists(mock_get_all_events):
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    cog = EventsCog(bot)

    await cog.createEvent.callback(cog, ctx=ctx, eventName="ExistingEvent", duration=5, start_date="01-01-2023", end_date="05-01-2023", token_reward=10)

    ctx.send.assert_called_once_with(f"Event with the name ExistingEvent already exists!")


@pytest.mark.asyncio
@patch('events_feature.db.get_all_events', return_value=[])
@patch('events_feature.db.add_event')
async def test_createEvent_successful_creation(mock_get_all_events,mock_add_event):
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    cog = EventsCog(bot)

    await cog.createEvent.callback(cog, ctx=ctx, eventName="NewEvent", duration=5, start_date="01-01-2023", end_date="05-01-2023", token_reward=10)

    ctx.send.assert_called_once_with(f"Event NewEvent created successfully!")

@pytest.mark.asyncio
async def test_deleteEvent_existing_event():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    cog = EventsCog(bot)

    # Mock the database call
    with patch('events_feature.db.get_all_events', return_value={"TestEvent": {}}):
        await cog.deleteEvent.callback(cog, ctx=ctx, eventName="TestEvent")

    ctx.send.assert_called_once_with("Event TestEvent deleted successfully!")

@pytest.mark.asyncio
async def test_deleteEvent_nonexistent_event():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    cog = EventsCog(bot)

    # Mock the database call
    with patch('events_feature.db.get_all_events', return_value={}):
        await cog.deleteEvent.callback(cog, ctx=ctx, eventName="TestEvent")

    ctx.send.assert_called_once_with("No event found with the name TestEvent!")

@pytest.mark.asyncio
async def test_deleteEvent_insufficient_permissions():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.command = Mock()
    ctx.command.name = "deleteEvent"

    cog = EventsCog(bot)

    # Simulate a MissingRole error
    error = commands.MissingRole("BotCommander")
    await cog.role_error(ctx, error)

    ctx.send.assert_called_once_with(f"{ctx.author.mention}, you do not have the necessary role to use this command.")

@pytest.mark.asyncio
async def test_listEvents_with_events():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database call to return a list of events
    events_data = {
        "Event1": {
            "duration": 5,
            "start_date": "01-01-2023",
            "end_date": "05-01-2023",
            "token_reward": 10
        },
        "Event2": {
            "duration": 7,
            "start_date": "10-01-2023",
            "end_date": "16-01-2023",
            "token_reward": 15
        }
    }

    with patch('events_feature.db.get_all_events', return_value=events_data):
        await cog.listEvents.callback(cog, ctx=ctx)

    # Check the response
    expected_response = (
        "List of events:\n"
        "Event Name: Event1, Duration: 5 days, Start: 01-01-2023, End: 05-01-2023, Token Reward: 10\n"
        "Event Name: Event2, Duration: 7 days, Start: 10-01-2023, End: 16-01-2023, Token Reward: 15\n"
    )
    ctx.send.assert_called_once_with(expected_response)

@pytest.mark.asyncio
async def test_listEvents_no_events():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database call to return an empty list
    with patch('events_feature.db.get_all_events', return_value={}):
        await cog.listEvents.callback(cog, ctx=ctx)

    # Check the response
    ctx.send.assert_called_once_with("No events found!")

# Testing for event !register
@pytest.mark.asyncio
async def test_register_already_registered():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.id = 12345  # Mock user ID
    ctx.message.author.mention = "@user"  # Mock user mention

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database call to indicate the user is already registered for the specific event
    with patch('events_feature.db.is_user_registered', return_value=True) as mock_is_registered:
        mock_is_registered.return_value = True
        await cog.register.callback(cog, ctx=ctx, event_name="TestEvent")

    # Check the response
    ctx.send.assert_called_once_with("@user, you are already registered for event TestEvent!")


@pytest.mark.asyncio
async def test_register_not_registered():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.id = 12345  # Mock user ID
    ctx.message.author.mention = "@user"  # Mock user mention

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database call to indicate the user is not registered for the specific event
    with patch('events_feature.db.is_user_registered', return_value=False) as mock_is_registered:
        # Also mock the database call to register the user
        with patch('events_feature.db.register_user'):
            await cog.register.callback(cog, ctx=ctx, event_name="TestEvent")

    # Check the response
    ctx.send.assert_called_once_with("@user, you have been successfully registered for event TestEvent!")


# Testing for event !post
@pytest.mark.asyncio
async def test_post_invalid_url():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.mention = "@user"  # Mock user mention

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Call the post command with an invalid URL
    await cog.post.callback(cog, ctx=ctx, event_name="TestEvent", url="https://invalid.url", for_which_day_posting=1, total_challenge_days=30)

    # Check the response
    ctx.send.assert_called_once_with("@user, please provide a URL in the format: https://www.linkedin.com/feed/update/urn:li:activity:<numeric_id>/")

@pytest.mark.asyncio
async def test_post_event_not_exist():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.mention = "@user"  # Mock user mention

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database call to indicate the user is not registered for the event
    with patch('events_feature.db.is_user_registered', return_value=True):
        # Mock the database call to indicate the event does not exist
        with patch('events_feature.db.get_all_events', return_value={}):
            await cog.post.callback(cog, ctx=ctx, event_name="NonexistentEvent", url="https://www.linkedin.com/feed/update/urn:li:activity:1234567890/", for_which_day_posting=1, total_challenge_days=30)

    # Check the response
    ctx.send.assert_called_once_with("No event found with the name NonexistentEvent!")


@pytest.mark.asyncio
async def test_post_user_not_registered():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.id = 12345  # Mock user ID
    ctx.message.author.mention = "@user"  # Mock user mention

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database call to indicate the user is not registered
    with patch('events_feature.db.is_user_registered', return_value=False):
        await cog.post.callback(cog, ctx=ctx, event_name="TestEvent", url="https://www.linkedin.com/feed/update/urn:li:activity:1234567890/", for_which_day_posting=1, total_challenge_days=30)

    # Check the response
    ctx.send.assert_called_once_with("@user, you need to register first using `!register` for this TestEvent.")

@pytest.mark.asyncio
async def test_post_valid_url_and_event():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.id = 12345  # Mock user ID
    ctx.message.author.mention = "@user"  # Mock user mention

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database calls
    with patch('events_feature.db.is_user_registered', return_value=True), \
         patch('events_feature.db.get_all_events', return_value={"TestEvent": {"start_date": "01-01-2023", "end_date": "30-01-2023"}}), \
         patch('events_feature.db.has_posted_today', side_effect=[False, True]):
        await cog.post.callback(cog, ctx=ctx, event_name="TestEvent", url="https://www.linkedin.com/feed/update/urn:li:activity:1234567890/", for_which_day_posting=1, total_challenge_days=30)

    # Check the response
    ctx.send.assert_called_once_with("@user, you can't post for this event today. Please check the event's date range.")

@pytest.mark.asyncio
async def test_post_twice_same_day():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.message = Mock()
    ctx.message.author = Mock()
    ctx.message.author.id = 12345  # Mock user ID
    ctx.message.author.mention = "@user"  # Mock user mention

    # Create an instance of the EventsCog
    cog = EventsCog(bot)

    # Mock the database calls
    with patch('events_feature.db.is_user_registered', return_value=True), \
         patch('events_feature.db.get_all_events', return_value={"TestEvent": {"start_date": "01-01-2023", "end_date": "30-01-2023"}}), \
         patch('events_feature.db.has_posted_today', side_effect=[False, True]):
        await cog.post.callback(cog, ctx=ctx, event_name="TestEvent", url="https://www.linkedin.com/feed/update/urn:li:activity:1234567890/", for_which_day_posting=1, total_challenge_days=30)
        await cog.post.callback(cog, ctx=ctx, event_name="TestEvent", url="https://www.linkedin.com/feed/update/urn:li:activity:1234567890/", for_which_day_posting=1, total_challenge_days=30)

    # Check the response for the second call
    ctx.send.assert_called_with("@user, you can't post for this event today. Please check the event's date range.")

# checkStreak
@pytest.mark.asyncio
async def test_checkStreak_user_has_posted():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.author.id = 12345  # Set a specific return value for ctx.author.id
    ctx.author.mention = "@user"  # Mock the mention attribute for the author

    # Mock the database functions
    mock_events = {
        "SampleEvent": {
            'duration': 7,
            'start_date': '01-01-2023',
            'end_date': '08-01-2023',
            'token_reward': 10
        }
    }

    with patch('events_feature.db.is_user_registered', return_value=True), \
            patch('events_feature.db.get_user_streak', return_value=5), \
            patch('events_feature.db.get_all_events', return_value=mock_events):
        # Create an instance of the EventsCog
        cog = EventsCog(bot)

        # Call the checkStreak function
        await cog.checkStreak.callback(cog, ctx, "SampleEvent")

        # Check that the bot sent the expected response
        expected_message = "@user, your current streak for `SampleEvent` is `5` days."
        ctx.send.assert_called_once_with(expected_message)


@pytest.mark.asyncio
async def test_checkStreak_user_has_not_posted():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.author.id = 12345  # Set a specific return value for ctx.author.id
    ctx.author.mention = "@user"  # Mock the mention attribute for the author

    # Mock the database functions
    mock_events = {
        "SampleEvent": {
            'duration': 7,
            'start_date': '01-01-2023',
            'end_date': '08-01-2023',
            'token_reward': 10
        }
    }

    with patch('events_feature.db.is_user_registered', return_value=True), \
            patch('events_feature.db.get_user_streak', return_value=0), \
            patch('events_feature.db.get_all_events', return_value=mock_events):
        # Create an instance of the EventsCog
        cog = EventsCog(bot)

        # Call the checkStreak function
        await cog.checkStreak.callback(cog, ctx, "SampleEvent")

        # Check that the bot sent the expected response
        expected_message = "@user, you haven't posted for the event `SampleEvent` yet."
        ctx.send.assert_called_once_with(expected_message)

@pytest.mark.asyncio
async def test_eligibility_without_eligible_users():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Mock the database functions
    with patch('events_feature.db.get_eligible_users', return_value=[]), \
         patch('events_feature.db.get_all_events', return_value={"SampleEvent": {}}):  # Mocking the event existence
        # Create an instance of the EventsCog
        cog = EventsCog(bot)

        # Call the eligibility function
        await cog.eligibility.callback(cog, ctx, "SampleEvent")

        # Check that the bot sent the expected response
        expected_message = "No users are currently eligible for the event `SampleEvent`."
        ctx.send.assert_called_once_with(expected_message)

@pytest.mark.asyncio
async def test_eligibility_insufficient_permissions():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()
    ctx.author.guild_permissions.administrator = False  # Mocking insufficient permissions

    # Mock the database functions
    with patch('events_feature.db.get_all_events', return_value={"SampleEvent": {}}):  # Mocking the event existence
        # Create an instance of the EventsCog
        cog = EventsCog(bot)

        # Call the eligibility function
        await cog.eligibility.callback(cog, ctx, "SampleEvent")

        # Check that the bot sent the expected response
        expected_message = "You don't have the necessary permissions to execute this command."
        ctx.send.assert_called_once_with(expected_message)


# Exporting_test_case
@pytest.mark.asyncio
async def test_export_eligible_users():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Mock the database function to return eligible users
    # eligible_users = [12345, 67890]

    mock_file = Mock()  # Create a mock object for the file

    with patch('events_feature.db.get_eligible_users',
               return_value=[{"user_id": 1, "streak": 5, "last_post_date": "01-01-2023"}]), \
            patch('events_feature.db.get_all_events', return_value={"SampleEvent": {}}), \
            patch('events_feature.ge.generate_excel', return_value="eligible_participants.xlsx"), \
            patch('discord.File', return_value=mock_file), \
            patch('os.path.exists', return_value=True):  # Mocking the os.path.exists function

        # Create an instance of the EventsCog
        cog = EventsCog(bot)

        # Call the export function
        await cog.export.callback(cog, ctx, "SampleEvent")

        # Check that the bot sent the expected response
        expected_message = "Here's the list of eligible participants for SampleEvent:"
        ctx.send.assert_called_once_with(expected_message, file=mock_file)  # Use the mock_file object in the assertion


@pytest.mark.asyncio
async def test_export_no_eligible_users():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Mock the database function to return no eligible users
    with patch('events_feature.db.get_eligible_users', return_value=[]), \
         patch('events_feature.db.get_all_events', return_value={"SampleEvent": {}}), \
         patch('events_feature.ge.generate_excel', return_value="eligible_participants.xlsx"), \
         patch('discord.File', Mock()):  # Mocking the File class from discord

        # Create an instance of the EventsCog
        cog = EventsCog(bot)

        # Call the export function
        await cog.export.callback(cog, ctx, "SampleEvent")

        # Check that the bot sent the expected response
        expected_message = f"No eligible users found for the event: SampleEvent."
        ctx.send.assert_called_once_with(expected_message)



# Test case for distributing tokens
@pytest.mark.asyncio
async def test_distribute_tokens_with_eligible_users():
    # 1. Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # 2. Mock the database function to return eligible users
    eligible_users = [
        {"user_id": 12345, "tokens": 100},
        {"user_id": 67890, "tokens": 100}
    ]

    with patch('events_feature.db.get_eligible_users', return_value=eligible_users), \
            patch('events_feature.db.get_all_events',
                  return_value={"SampleEvent": {}}),\
            patch('events_feature.db.distribute_tokens', return_value=True) as mock_distribute_tokens:

    # Create an instance of the EventsCog or whichever class contains the distribute function
        cog = EventsCog(bot)

        # 4. Call the function that distributes the tokens
        await cog.distribute_tokens.callback(cog, ctx, "SampleEvent")

        # 5. Check that the tokens were distributed as expected
        mock_distribute_tokens.assert_called_once_with("SampleEvent")

        ctx.send.assert_called_once_with("Tokens have been distributed for the event: SampleEvent")

@pytest.mark.asyncio
async def test_distribute_tokens_no_eligible_users():
    # Mock the bot and context
    bot = Mock()
    ctx = Mock()
    ctx.send = AsyncMock()

    # Mock the database function to return no eligible users
    with patch('events_feature.db.get_eligible_users', return_value=[]), \
         patch('events_feature.db.get_all_events', return_value={"SampleEvent": {}}):

        # Create an instance of the EventsCog
        cog = EventsCog(bot)

        # Call the distribute_tokens function
        await cog.distribute_tokens.callback(cog, ctx, "SampleEvent")

        # Check that the bot sent the expected response
        expected_message = "No eligible users found for the event: SampleEvent."
        ctx.send.assert_called_once_with(expected_message)
