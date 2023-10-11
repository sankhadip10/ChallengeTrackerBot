from discord.ext import commands

def setup_reactions(bot):

    @bot.event
    async def on_message(message):
        # Ensure the bot doesn't respond to its own messages
        if message.author == bot.user:
            return

        # Your reactions logic here, e.g., 
        if message.content.startswith("Report"):
            await message.add_reaction("👍")
        else:
            await message.delete()
            warning = await message.channel.send(f"{message.author.mention}, your message does not start with 'Report'. Please follow the correct format.")
            # Optionally, delete the warning after a few seconds for cleanliness
            await warning.delete(delay=5)

    # If you had other functionalities related to reactions, you can define them here.
