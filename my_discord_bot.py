import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user:  # ignore bot's own messages
        return

    content = message.content
    print(f"Received message from {message.author.name}: {content}")

    if not content.startswith("Report"):
        await message.delete()
        warn_msg = await message.channel.send(f"{message.author.mention}, your message is in the wrong format.")
        await warn_msg.delete(delay=5)  # this deletes the warning message after 5 seconds
    else:
        await message.add_reaction('👍')

    await bot.process_commands(message)  # to allow command processing

bot.run('MTE2MTcxMTY0MTYzNzk2MTg1OQ.Gqhkmp.Eh1YbStDeS4kDFCWfxQixQ4bLS_aYyM7g0JCjY')
