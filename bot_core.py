import discord
from discord.ext import commands
from config import BOT_TOKEN
import asyncio  # Import the asyncio module

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}({bot.user.id})')
    if not hasattr(bot, 'extensions_loaded'):
        await load_extensions()
        bot.extensions_loaded = True


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

if __name__ == "__main__":
    # asyncio.run(load_extensions())
    keep_alive()
    bot.run(BOT_TOKEN)