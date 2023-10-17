import re,os,sqlite3
from datetime import date,datetime
import validators
import discord
from discord.ext import commands
import post_verification
import database as db
import generate_excel as ge

PAGE_SIZE = 20  # Number of users displayed per page
current_pages = {}
class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("BotCommander")
    async def createEvent(self, ctx, eventName: str, duration: int, start_date: str, end_date: str, token_reward: int):
        # Validate event name
        if not (3 <= len(eventName) <= 50):  # Assuming a min length of 3 and max length of 50
            await ctx.send("Event name should be between 3 and 50 characters long.")
            return

        # Check for invalid characters in the event name
        valid_characters = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")
        if not set(eventName).issubset(valid_characters):
            await ctx.send(
                "Event name contains invalid characters. Only alphanumeric characters, hyphens, and underscores are allowed.")
            return
        # Date validation
        date_format = "%d-%m-%Y"  # This format represents "DD-Month-YYYY"
        try:
            start = datetime.strptime(start_date, date_format).date()
            end = datetime.strptime(end_date, date_format).date()
        except ValueError:
            await ctx.send("The date format is incorrect! Please use DD-Month-YYYY format (e.g., 15-10-2023).")
            return

        # Check if duration matches the difference between start and end dates
        calculated_duration = (end - start).days + 1  # +1 to include both start and end dates
        if calculated_duration != duration:
            await ctx.send(
                f"The provided duration doesn't match the start and end dates. It should be {duration} days,instead its giving difference {calculated_duration} days.")
            return

        try:
            if eventName in db.get_all_events():
                await ctx.send(f"Event with the name {eventName} already exists!")
                return

            # Store the event in the database
            db.add_event(eventName, duration, start_date, end_date, token_reward)
            await ctx.send(f"Event {eventName} created successfully!")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Handle cog-specific errors
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("This command does not exist!")
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.name == "post":
                await ctx.send(
                    f"You're missing the `{error.param.name}` argument for this command! The correct format is: `!post <event_name> <url> <for_which_day_posting> <total_challenge_days>`.")
            else:
                await ctx.send(f"You're missing the `{error.param.name}` argument for this command!")
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            # Get the command's signature to show the correct format
            command_signature = ctx.command.signature
            await ctx.send(
                f"You're missing the `{error.param.name}` argument for this command! The correct format is: `!{ctx.command.name} {command_signature}`.")
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You're missing the {error.param.name} argument for this command!")
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You're missing the {error.param.name} argument for this command!")
            return
        elif isinstance(error, commands.BadArgument):
            await ctx.send("One of the arguments you provided is invalid. Please check and try again.")
            return
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An unexpected error occurred. Please try again later.")
            return
        elif isinstance(error, commands.BotMissingPermissions):
            missing_permissions = ", ".join(
                [str(perm.replace("_", " ").replace("guild", "server").title()) for perm in
                 error.missing_permissions])
            await ctx.send(f"I'm missing the following permissions: {missing_permissions}")

        elif isinstance(error, discord.HTTPException) and error.status == 429:
            await ctx.send("I'm being rate limited by Discord right now. Please try again in a few seconds.")
        # If the error is not handled above, call the bot's main error handler
        await self.bot.on_command_error(ctx, error)

    @commands.command()
    @commands.has_role("BotCommander")
    # @commands.has_permissions(administrator=True)
    async def deleteEvent(self, ctx, eventName: str):
        try:
            if eventName not in db.get_all_events():
                await ctx.send(f"No event found with the name {eventName}!")
                return

            db.delete_event(eventName)  # Assuming a function to delete an event
            await ctx.send(f"Event {eventName} deleted successfully!")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def listEvents(self,ctx):
        print(f"listEvents command triggered by {ctx.author.name}")
        try:
            events = db.get_all_events()
            if not events:
                await ctx.send("No events found!")
                return

            response = "List of events:\n"
            for event, details in events.items():
                response += (f"Event Name: {event}, Duration: {details['duration']} days, "
                             f"Start: {details['start_date']}, End: {details['end_date']}, "
                             f"Token Reward: {details['token_reward']}\n")

            await ctx.send(response)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def register(self,ctx):
        user_id = ctx.message.author.id
        if db.is_user_registered(user_id):  # You need to define this function in your database.py
            await ctx.send(f"{ctx.message.author.mention}, you are already registered!")
            return
        db.register_user(user_id)  # Register the user in your data storage
        await ctx.send(f"{ctx.message.author.mention}, you have been successfully registered!")


    @commands.command()
    async def post(self,ctx, event_name: str, url: str, for_which_day_posting: int, total_challenge_days: int):
        user_id = ctx.message.author.id

        # Check URL format
        pattern = r'^https://www\.linkedin\.com/feed/update/urn:li:activity:[0-9]+/$'
        if not re.match(pattern, url):
            await ctx.send(
                f"{ctx.message.author.mention}, please provide a URL in the format: https://www.linkedin.com/feed/update/urn:li:activity:<numeric_id>/")
            return

        if not db.is_user_registered(user_id):
            await ctx.send(f"{ctx.message.author.mention}, you need to register first using `!register`.")
            return

        # Check if event exists
        event_details = db.get_all_events().get(event_name)
        if not event_details:
            await ctx.send(f"No event found with the name {event_name}!")
            return



        if not validators.url(url):
            await ctx.send(f"{ctx.message.author.mention}, the provided URL is not valid.")
            return

        # Check if the current date is within the event's start and end dates
        current_date = date.today()
        start_date = datetime.strptime(event_details['start_date'], "%d-%m-%Y").date()
        end_date = datetime.strptime(event_details['end_date'], "%d-%m-%Y").date()
        if start_date > current_date or end_date < current_date:
            await ctx.send(
                f"{ctx.message.author.mention}, you can't post for this event today. Please check the event's date range.")
            return
        # Check for duplicate posts (assuming you have a function in your database module for this)
        if db.has_posted_today(user_id, event_name, date.today()):
            await ctx.send(f"{ctx.message.author.mention}, you've already posted for this event today.")
            return
        # Validate day numbers
        if not (1 <= for_which_day_posting <= event_details['duration']):
            await ctx.send(f"{ctx.message.author.mention}, the day number you provided is out of range for this event.")
            return

        # Verify the post
        is_verified = post_verification.PostVerification.verify_post(url, for_which_day_posting, total_challenge_days)
        if not is_verified:
            await ctx.send(f"{ctx.message.author.mention}, the URL provided didn't match our verification criteria.")
            return

            # Handle potential database errors
        try:
            db.add_daily_post(user_id, url)
            db.update_streak(user_id, event_name, date.today())
            await ctx.send(
                f"{ctx.message.author.mention}, your post has been recorded for today for the event {event_name}!")
        except Exception as e:
            await ctx.send(
                f"{ctx.message.author.mention}, an error occurred while recording your post. Please try again later.")

    @commands.command()
    async def checkStreak(self, ctx, event_name: str):
        user_id = ctx.author.id

        # Check if user is registered
        if not db.is_user_registered(user_id):
            await ctx.send(f"{ctx.author.mention}, you need to register first using `!register`.")
            return

        # Check if event exists
        if event_name not in db.get_all_events():
            await ctx.send(f"No event found with the name {event_name}!")
            return

        try:
            streak = db.get_user_streak(user_id, event_name)

            # Check if user has posted for the event
            if streak == 0:
                await ctx.send(f"{ctx.author.mention}, you haven't posted for the event `{event_name}` yet.")
                return

            await ctx.send(f"{ctx.author.mention}, your current streak for `{event_name}` is `{streak}` days.")
        except Exception as e:
            await ctx.send(f"An error occurred while fetching your streak: {e}")



    @commands.command()
    @commands.has_role("BotCommander")
    async def eligibility(self, ctx, event_name: str, page: int = 1):
        try:
            if not ctx.author.guild_permissions.administrator:
                await ctx.send("You don't have the necessary permissions to execute this command.")
                return
            # Check if the event exists
            if event_name not in db.get_all_events():
                await ctx.send(f"No event found with the name {event_name}!")
                return

            eligible_users = db.get_eligible_users(event_name)
            if not eligible_users:
                await ctx.send(f"No users are currently eligible for the event `{event_name}`.")
                return

            eligible_mentions = [f"<@{user_id}>" for user_id in eligible_users]

            start_index = (page - 1) * PAGE_SIZE
            end_index = start_index + PAGE_SIZE

            current_page_users = eligible_mentions[start_index:end_index]

            if not current_page_users:
                await ctx.send(f"No more eligible users to display for page {page}.")
                return

            response = f"Eligible users for `{event_name}` (Page {page}):\n" + ", ".join(current_page_users)
            await ctx.send(response)

            # Store the current page for this context
            current_pages[(ctx.channel.id, ctx.author.id)] = page

        except Exception as e:
            await ctx.send(f"An error occurred while fetching eligible users: {e}")

    @eligibility.error
    async def eligibility_error(self,ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"{ctx.author.mention}, you do not have the necessary role to use this command.")

    @commands.has_role("BotCommander")
    @commands.command(name='export')
    async def export(self, ctx, event_name: str):
        try:
            if "BotCommander" not in [role.name for role in ctx.author.roles]:
                await ctx.send("You don't have the necessary permissions to execute this command.")
                return

            # Check if the event exists
            if event_name not in db.get_all_events():
                await ctx.send(f"No event found with the name {event_name}!")
                return

            eligible_users = db.get_eligible_users(event_name)
            if not eligible_users:
                await ctx.send(f"No eligible users found for the event: {event_name}.")
                return

            # Generate the Excel file
            filename = ge.generate_excel(eligible_users)

            if not os.path.exists(filename):
                await ctx.send("There was an error generating the Excel file. Please try again later.")
                return

            # Send the file to the Discord channel
            await ctx.send(f"Here's the list of eligible participants for {event_name}:", file=discord.File(filename))

        except sqlite3.Error as e:
            await ctx.send(f"Database error: {e}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.has_role("BotCommander")
    @commands.command(name="distributeTokens")
    async def distribute_tokens(self, ctx, event_name):
        try:
            if "BotCommander" not in [role.name for role in ctx.author.roles]:
                await ctx.send("You don't have the necessary permissions to execute this command.")
                return
            # Check if the event exists
            if event_name not in db.get_all_events():
                await ctx.send(f"No event found with the name {event_name}!")
                return

            eligible_users = db.get_eligible_users(event_name)
            if not eligible_users:
                await ctx.send(f"No eligible users found for the event: {event_name}.")
                return

            db.distribute_tokens(event_name)
            await ctx.send(f"Tokens have been distributed for the event: {event_name}")

        except sqlite3.Error as e:
            await ctx.send(f"Database error: {e}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @createEvent.error
    @deleteEvent.error
    @eligibility.error
    @export.error
    @distribute_tokens.error
    async def role_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"{ctx.author.mention}, you do not have the necessary role to use this command.")


# Ensure to load the commands when importing the module
async def setup(bot):
    await bot.add_cog(EventsCog(bot))

