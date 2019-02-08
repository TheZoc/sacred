'''
This file handles the messages in #welcome channel and handles when users
accept the terms via the `!accept` command.

Any other messages typed by non whitelisted users will be deleted by the bot.
'''

import discord
import bot_config as config
from modules import logger


async def welcome_channel_handler(client, message):
    '''Handles the messages sent in the #welcome channel'''
    if (config.welcome_channel_id != message.channel.id):
        return False

    if message.content.startswith('!accept'):
        return await user_accepted_terms(client, message)
    else:
        return await delete_unwanted_welcome_messages(client, message)


async def user_accepted_terms(client, message):
    '''Add the user to the specified role'''
    logMessage = '[!accept]' + \
        ' User ' + message.author.name + '#' + message.author.discriminator + \
        ' has accepted the terms.'
    logger.info(logMessage)

    # Set the user role. If not possible, log it.
    try:
        member_role = discord.utils.get(message.guild.roles, id=config.member_role_id)
        await message.author.add_roles(member_role, reason='User accepted terms')

    except discord.Forbidden:
        logger.error('[!accept] Insufficient permission to add the specified role to the user.')

    except discord.HTTPException:
        logger.error("[!accept] HTTPException (?!)")

    # Delete the user message. If not possible, log it.
    try:
        await message.delete()

    except discord.Forbidden:
        logger.error('[!accept] Insufficient permission to delete the specified user message.')

    except discord.HTTPException:
        logger.error("[!accept] HTTPException (?!)")

    # Message handled
    return True


async def delete_unwanted_welcome_messages(client, message):
    '''Delete every message on #welcome that is not from a whitelisted user'''

    # Check to see if the user who sent the message is on the whitelist. If not, delete it.
    if (set([role.id for role in message.author.roles]).isdisjoint(config.welcome_allowed_roles_msg)):
        try:
            await message.delete()

        except discord.Forbidden:
            logger.error('[unwanted welcome msg] Insufficient permission to delete the specified user message.')

        except discord.HTTPException:
            logger.error("[unwanted welcome msg] HTTPException (?!)")

    # Message Handled
    return True
