from discord.ext import commands
import database as db  # If you're using a separate database.py file


def setup_events(bot):
    @bot.command()
    async def createEvent(ctx, eventName, duration: int):
        if eventName in db.get_all_events():  # Assuming a function to get all events from the database
            await ctx.send(f"Event with the name {eventName} already exists!")
            return

        # Store the event in the database
        db.add_event(eventName, duration)  # Function to add an event to the database
        await ctx.send(f"Event {eventName} created successfully!")

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def deleteEvent(ctx, eventName):
        if eventName not in db.get_all_events():
            await ctx.send(f"No event found with the name {eventName}!")
            return

        db.delete_event(eventName)  # Function to delete an event from the database
        await ctx.send(f"Event {eventName} deleted successfully!")

    @bot.command()
    async def listEvents(ctx):
        events = db.get_all_events()  # Function to get all events from the database
        if not events:
            await ctx.send("No events found!")
            return

        response = "List of events:\n"
        for event, details in events.items():
            response += f"Event Name: {event}, Duration: {details['duration']} days, Start: {details['start_date']}, End: {details['end_date']}\n"

        await ctx.send(response)

    # Add any other event-related functionalities if needed
