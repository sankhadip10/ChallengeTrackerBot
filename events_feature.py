from datetime import date,datetime
import discord
from discord.ext import commands
import post_verification
import database as db
import generate_excel as ge


class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("BotCommander")
    async def createEvent(self,ctx, eventName: str, duration: int, start_date: str, end_date: str):
        # Date validation
        date_format = "%d-%m-%Y"  # This format represents "DD-Month-YYYY"
        try:
            datetime.strptime(start_date, date_format)
            datetime.strptime(end_date, date_format)
        except ValueError:
            await ctx.send("The date format is incorrect! Please use DD-Month-YYYY format (e.g., 15-10-2023).")
            return

        try:
            if eventName in db.get_all_events():
                await ctx.send(f"Event with the name {eventName} already exists!")
                return

            # Store the event in the database
            db.add_event(eventName, duration, start_date, end_date)
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
            await ctx.send(f"You're missing the {error.param.name} argument for this command!")
            return
        # If the error is not handled above, call the bot's main error handler
        await self.bot.on_command_error(ctx, error)

    @commands.command()
    @commands.has_role("BotCommander")
    # @commands.has_permissions(administrator=True)
    async def deleteEvent(self,ctx, eventName: str):
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
        try:
            events = db.get_all_events()
            if not events:
                await ctx.send("No events found!")
                return

            response = "List of events:\n"
            for event, details in events.items():
                response += f"Event Name: {event}, Duration: {details['duration']} days, Start: {details['start_date']}, End: {details['end_date']}\n"

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
    async def post(self,ctx, event_name: str, url: str, no_of_day: int, total_challenge_days: int):
        user_id = ctx.message.author.id

        # Check if event exists
        if event_name not in db.get_all_events():
            await ctx.send(f"No event found with the name {event_name}!")
            return

        if not db.is_user_registered(user_id):
            await ctx.send(f"{ctx.message.author.mention}, you need to register first using `!register`.")
            return

        # Verify the post
        is_verified = post_verification.PostVerification.verify_post(url, no_of_day, total_challenge_days)
        if not is_verified:
            await ctx.send(f"{ctx.message.author.mention}, the URL provided didn't match our verification criteria.")
            return

        db.add_daily_post(user_id, url)
        db.update_streak(user_id, event_name, date.today())  # Update the streak
        await ctx.send(
            f"{ctx.message.author.mention}, your post has been recorded for today for the event {event_name}!")

    @commands.command()
    async def checkStreak(self,ctx, event_name: str):
        user_id = ctx.author.id
        streak = db.get_user_streak(user_id, event_name)
        await ctx.send(f"{ctx.author.mention}, your current streak for `{event_name}` is `{streak}` days.")

    @commands.command()
    @commands.has_role("BotCommander")
    async def eligibility(self,ctx, event_name: str):
        eligible_users = db.get_eligible_users(event_name)
        if not eligible_users:
            await ctx.send(f"No users are currently eligible for the event `{event_name}`.")
            return

        eligible_mentions = [f"<@{user_id}>" for user_id in eligible_users]
        response = f"Eligible users for `{event_name}`:\n" + ", ".join(eligible_mentions)
        await ctx.send(response)

    @eligibility.error
    async def eligibility_error(self,ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send(f"{ctx.author.mention}, you do not have the necessary role to use this command.")

    @commands.command(name='export')
    @commands.has_role("BotCommander")  # Only allow admins to run this command
    async def export(self,ctx, event_name: str):
        # Fetch eligible users from the database for the given event_name
        eligible_users = db.get_eligible_users(event_name)

        if not eligible_users:
            await ctx.send(f"No eligible users found for the event: {event_name}.")
            return

        # Generate the Excel file
        filename = ge.generate_excel(eligible_users)

        # Send the file to the Discord channel
        await ctx.send(f"Here's the list of eligible participants for {event_name}:", file=discord.File(filename))

    @commands.command(name="distributeTokens")
    @commands.has_role("BotCommander")      # Ensure only moderators can use this
    async def distribute_tokens(self,ctx, event_name):
        try:
            db.distribute_tokens(event_name)
            await ctx.send(f"Tokens have been distributed for the event: {event_name}")
        except Exception as e:
            await ctx.send(f"Error distributing tokens: {e}")


# Ensure to load the commands when importing the module
def setup(bot):
    bot.add_cog(EventsCog(bot))
