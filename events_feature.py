from discord.ext import commands
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


# Ensure to load the commands when importing the module
def setup(bot):
    bot.add_cog(setup(bot))
