import discord
from discord.ext import commands
from config import BOT_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension("reactions_feature")
    await bot.load_extension("events_feature")
    print(f'Logged in as {bot.user.name}({bot.user.id})')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Sorry {ctx.author.mention}, that command doesn't exist!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You're missing a required argument for this command!")
    else:
        await ctx.send(f"An error occurred: {error}")


# Load the events feature as an extension (cog)
# bot.load_extension("reactions_feature")
# bot.load_extension("events_feature")
# bot.load_extension("post_verification")


if __name__ == "__main__":
    bot.run(BOT_TOKEN)
