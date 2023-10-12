import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_message(message):
    if message.author == bot.user or isinstance(message.channel, discord.DMChannel):  # ignore bot's own messages and DMs
        return

    content = message.content
    print(f"Received message from {message.author.name}: {content}")

    if not content.startswith("Report"):
        try:
            await message.delete()
            warn_msg = await message.channel.send(f"{message.author.mention}, your message is in the wrong format.")
            await warn_msg.delete(delay=5)
        except discord.Forbidden:
            await message.channel.send("I don't have the necessary permissions.")
    else:
        try:
            await message.add_reaction('👍')
        except discord.Forbidden:
            await message.channel.send("I don't have permission to react to messages.")

    await bot.process_commands(message)


bot.run('MTE2MTcxMTY0MTYzNzk2MTg1OQ.Gqhkmp.Eh1YbStDeS4kDFCWfxQixQ4bLS_aYyM7g0JCjY')
