from datetime import datetime

from discord.ext import commands
import post_verification
import database as db


def setup_events(bot):
    @bot.command()
    async def createEvent(ctx, eventName: str, duration: int, start_date: str, end_date: str):
        try:
            if eventName in db.get_all_events():
                await ctx.send(f"Event with the name {eventName} already exists!")
                return

            # Store the event in the database
            db.add_event(eventName, duration, start_date, end_date)
            await ctx.send(f"Event {eventName} created successfully!")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def deleteEvent(ctx, eventName: str):
        try:
            if eventName not in db.get_all_events():
                await ctx.send(f"No event found with the name {eventName}!")
                return

            db.delete_event(eventName)  # Assuming a function to delete an event
            await ctx.send(f"Event {eventName} deleted successfully!")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @bot.command()
    async def listEvents(ctx):
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

    # Assuming you've already imported the necessary modules and set up your bot
    @bot.command()
    async def register(ctx):
        user_id = ctx.message.author.id
        if db.is_user_registered(user_id):  # You need to define this function in your database.py
            await ctx.send(f"{ctx.message.author.mention}, you are already registered!")
            return
        db.register_user(user_id)  # Register the user in your data storage
        await ctx.send(f"{ctx.message.author.mention}, you have been successfully registered!")

    # @bot.command()
    # async def post(ctx, url: str):
    #     user_id = ctx.message.author.id
    #     if not db.is_user_registered(user_id):
    #         await ctx.send(f"{ctx.message.author.mention}, you need to register first using `!register`.")
    #         return
    #     db.add_daily_post(user_id, url)  # You need to define this function in your database.py
    #     await ctx.send(f"{ctx.message.author.mention}, your post has been recorded for today!")

    @bot.command()
    async def post(ctx, event_name: str, url: str):
        user_id = ctx.message.author.id

        # Check if event exists
        if event_name not in db.get_all_events():
            await ctx.send(f"No event found with the name {event_name}!")
            return

        if not db.is_user_registered(user_id):
            await ctx.send(f"{ctx.message.author.mention}, you need to register first using `!register`.")
            return

        # Verify the post
        is_verified = post_verification.verify_post(url)
        if not is_verified:
            await ctx.send(f"{ctx.message.author.mention}, the URL provided didn't match our verification criteria.")
            return

        db.add_daily_post(user_id, url)
        db.update_streak(user_id, event_name, datetime.date.today())  # Update the streak
        await ctx.send(
            f"{ctx.message.author.mention}, your post has been recorded for today for the event {event_name}!")


# Ensure to load the commands when importing the module
def setup(bot):
    bot.add_cog(setup(bot))
