import discord
from discord.ext import commands
import os
from typing import final
import glob

DISCORD_BOT_TOKEN: final(str) = os.getenv('DISCORD_BOT_TOKEN')
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())


async def load_extensions():
    for name in glob.glob('cog/?*/source/main.py'):
        extension_name = name[:len(name) - 3].replace('/', '.')
        await bot.load_extension(name=extension_name)
        print('cog "{0}" loaded.'.format(extension_name))


@bot.event
async def on_ready():
    await load_extensions()


bot.run(DISCORD_BOT_TOKEN)
