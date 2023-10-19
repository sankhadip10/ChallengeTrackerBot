import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

TOKEN = 'MTE2MTcxMTY0MTYzNzk2MTg1OQ.G_iKHQ.pP8sxL2VPR4P2BTlw4mO3pIPhxkRY9jmHGXwII'
bot = commands.Bot(command_prefix='!',intents=intents)
true_permissions = []
false_permissions = []
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name="Sankhadip's server")  # Replace with your server name
    member = guild.get_member(bot.user.id)
    # permissions = member.guild_permissions
    # for name, value in permissions:
    #     print(f"{name}: {value}")
    permissions = member.guild_permissions
    for name, value in permissions:
        if value:
            true_permissions.append(name)
        else:
            false_permissions.append(name)

    print("Permissions set to True:", ', '.join(true_permissions))
    print("Permissions set to False:", ', '.join(false_permissions))

bot.run(TOKEN)