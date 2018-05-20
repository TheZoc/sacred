#!/usr/bin/python3

import discord
import logging
import logging.handlers
import bot_config

# Setup logging. Very hackish for now, but I don't want to delay the discord announcement anymore.
# TODO: Create a class for async log handling
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
maxLogSize = 20 * 1024 * 1024
logBackupAmount = 20
logName = 'discord.log'
handler = logging.handlers.RotatingFileHandler(filename=logName, encoding='UTF-8', maxBytes=maxLogSize, backupCount=logBackupAmount)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Get Discord Client
client = discord.Client()


async def print_role_ids():
    """Utility Function: Print all the roles IDs from all connected servers"""
    for s in client.servers:
        print(s)
        for r in s.roles:
            print('\t' + r.name + ' = ' + r.id)


async def user_accepted_terms(message):
    """Add the user to the specified role"""
    if (bot_config.get_welcome_channel_id() == message.channel.id):
        logMessage = '[!accept]' + \
            ' User ' + message.author.name + '#' + message.author.discriminator + \
            ' has accepted the terms.'
        logger.info(logMessage)

        try:
            member_role = discord.utils.get(message.server.roles, id=bot_config.get_member_role_id())
            await client.add_roles(message.author, member_role)

        except discord.Forbidden:
            logger.error('[!accept] Insufficient permission to add the specified role to the user.')
            return

        except discord.HTTPException:
            logger.error("[!accept] HTTPException (?!)")
            return

        try:
            await client.delete_message(message)

        except discord.Forbidden:
            logger.error('[!accept] Insufficient permission to delete the specified user message.')
            return

        except discord.HTTPException:
            logger.error("[!accept] HTTPException (?!)")
            return


async def delete_unwanted_welcome_messages(message):
    if (bot_config.get_welcome_channel_id() == message.channel.id):
        if (set([role.id for role in message.author.roles]).isdisjoint(bot_config.roles_allowed_to_msg_welcome_channel())):
            try:
                await client.delete_message(message)

            except discord.Forbidden:
                logger.error('[unwanted welcome msg] Insufficient permission to delete the specified user message.')
                return

            except discord.HTTPException:
                logger.error("[unwanted welcome msg] HTTPException (?!)")
                return


# Setup on_ready() hook
@client.event
async def on_ready():
    print('Logged in as', end=' ')
    print(client.user.name + "#" + client.user.discriminator)
    await client.change_presence(game=discord.Game(name='Haven Alpha'))  # tee-hee


# Setup on_message() hook
@client.event
async def on_message(message):
    if message.content.startswith('!accept'):
        await user_accepted_terms(message)
    else:
        await delete_unwanted_welcome_messages(message)

# Run the bot!
client.run(bot_config.get_bot_token())
