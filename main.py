#!/usr/bin/env python
import os
import discord
import logging
from discord.ext import commands

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

shodan = commands.Bot(command_prefix='!')

@shodan.event
async def on_ready():
    guild = discord.utils.get(shodan.guilds, name=GUILD)

    logger.info(
            f'{shodan.user} is connected to:\n'
            f'{guild.name}(id: {guild.id})'
            )

    members = '\n - '.join([member.name for member in guild.members])
    logger.info(f'Members:\n - {members}')

@shodan.event
async def on_message(message):
    if message.author == shodan.user:
        return
    else:
        author = message.author
        logger.info(f'Message from {author.display_name}({author}): {message.content}')

    if any(x in message.content.lower() for x in ['ciao', 'ciao!']) or all(y in message.content.lower() for y in ['ciao', 'shodan']):
        response = f'Ciao {author.display_name}!'
        await message.channel.send(response)

shodan.run(TOKEN)
