import discord
from discord.ext import commands
from config import BOT_TOKEN
import asyncio  # Import the asyncio module

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}({bot.user.id})')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Sorry {ctx.author.mention}, that command doesn't exist!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument for this command!")
    else:
        await ctx.send(f"An error occurred: {error}")

async def load_extensions():
    await bot.load_extension("reactions_feature")
    await bot.load_extension("events_feature")




# Use asyncio to get the default event loop and run the coroutine
# loop = asyncio.get_event_loop()
# loop.run_until_complete(load_extensions())
asyncio.run(load_extensions())


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
