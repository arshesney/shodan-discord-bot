#!/usr/bin/env python
import os
import re
import random
import discord
import logging
import configparser
from discord.ext import commands

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CONFIG = os.getenv('SHODAN_CONFIG')

config = configparser.ConfigParser()
config.read(CONFIG)

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

    # continue with command processing
    await shodan.process_commands(message)

@shodan.command(name='roll', help='Dimmi che dadi tirare (tipo 3d6)')
async def roll(ctx, dice):
    formato = re.compile('[0-9]{1,3}d[0-9]{1,3}')
    logger.info(f'Roll comand with {dice}')
    if formato.match(dice) is None:
        ctx.send('Non ho capito')
        return

    total = 0
    num, faces = dice.split('d')
    dice_roll = [
            random.choice(range(1, int(faces) + 1))
            for _ in range(int(num))
            ]
    result = ''.join(str(dice_roll))
    print(result)
    if int(num) > 1:
        total = sum(dice_roll)
        result = result + f' totale: {total}'
    await ctx.send(result)

shodan.run(TOKEN)
