'''
This file handles the messages `!pugme` and `!unpugme`
and add the messenger to the pug group.
'''

import discord
import bot_config as config
from modules.logger import logger


async def sfc_pug_handler(client, message):
    '''Handles the messages sent in the #welcome channel'''
    if (message.channel.id not in config.sfcpugger_allowed_channels):
        return False

    if message.content.startswith('!pugme'):
        return await add_pugger(client, message)
    elif message.content.startswith('!unpugme'):
        return await remove_pugger(client, message)


async def add_pugger(client, message):
    '''Add the user to the specified role'''

    # Skiping logs for now
#    logMessage = '[!pugme]' + \
#        ' User ' + message.author.name + '#' + message.author.discriminator + \
#        ' asked to be a pugger.'
#    logger.info(logMessage)

    # Set the user role. If not possible, log it.
    try:
        pugger_role = discord.utils.get(message.guild.roles, id=config.sfcpugger_role_id)
        await message.author.add_roles(pugger_role, reason='User asked to be added to the SourceForts Classic pug group')

    except discord.Forbidden:
        logger.error('[!pugme] Insufficient permission to add the specified role to the user.')

    except discord.HTTPException:
        logger.error("[!pugme] HTTPException (?!)")

    # Message handled
    return True


async def remove_pugger(client, message):
    '''Add the user to the specified role'''

    # Skiping logs for now
#    logMessage = '[!pugme]' + \
#        ' User ' + message.author.name + '#' + message.author.discriminator + \
#        ' asked to be a pugger.'
#    logger.info(logMessage)

    # Set the user role. If not possible, log it.
    try:
        pugger_role = discord.utils.get(message.guild.roles, id=config.sfcpugger_role_id)
        await message.author.remove_roles(pugger_role, reason='User asked to be removed from the SourceForts Classic pug group')

    except discord.Forbidden:
        logger.error('[!pugme] Insufficient permission to add the specified role to the user.')

    except discord.HTTPException:
        logger.error("[!pugme] HTTPException (?!)")

    # Message handled
    return True

