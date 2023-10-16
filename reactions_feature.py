from discord.ext import commands

class ReactionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ensure the bot doesn't respond to its own messages or any bot's messages
        if message.author.bot:
            return

        # If the message is a command, process it and exit the function
        if message.content.startswith('!'):
            await self.bot.process_commands(message)
            return

        # Your reactions logic here
        if message.content.startswith("Report"):
            await message.add_reaction("👍")
        else:
            await message.delete()
            warning = await message.channel.send(
                f"{message.author.mention}, your message does not start with 'Report'. Please follow the correct format.")
            # Optionally, delete the warning after a few seconds for cleanliness
            await warning.delete(delay=5)


def setup(bot):
    bot.add_cog(ReactionsCog(bot))
