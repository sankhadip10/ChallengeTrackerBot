import discord
from discord.ext import commands
from reactions_feature import setup_reactions
from events_feature import setup_events
from config import BOT_TOKEN, DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Sorry {ctx.author.mention}, that command doesn't exist!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument for this command!")
    else:
        await ctx.send(f"An error occurred: {error}")

# Set up different features
setup_reactions(bot)
setup_events(bot)

if __name__ == "__main__":
    # from config import BOT_TOKEN
    bot.run(BOT_TOKEN)
    # db.add_event("Test Event", 10, "Start", "End")
    # print(db.get_all_events())