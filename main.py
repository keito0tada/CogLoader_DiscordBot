import discord
import psycopg2
from discord.ext import commands
import os, sys
from typing import Final
import glob
import logging

DISCORD_BOT_TOKEN: Final[str] = os.getenv('DISCORD_BOT_TOKEN')
DATABASE_URL: Final[str] = os.getenv('DATABASE_URL')


class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.database_connector = psycopg2.connect(DATABASE_URL)
    
bot = Bot(command_prefix='/', intents=discord.Intents.all())

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

async def load_extensions():
    log.info('load extensions')
    for name in glob.glob('cog/?*/source/main.py'):
        extension_name = name[:len(name) - 3].replace('/', '.')
        await bot.load_extension(name=extension_name)
        log.info('cog "{0}" loaded.'.format(extension_name))
    for name in glob.glob('cog/?*/src/main.py'):
        extension_name = name[:len(name) - 3].replace('/', '.')
        await bot.load_extension(name=extension_name)
        log.info('cog "{0}" loaded.'.format(extension_name))


@bot.event
async def on_ready():
    log.info('on ready')
    await load_extensions()
    await bot.tree.sync()


bot.run(DISCORD_BOT_TOKEN)
