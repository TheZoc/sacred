#!/usr/local/bin/python3
import asyncio
import sys
import signal
import discord
import bot_config as config
from modules import message_handlers, logger, setupLogger, addSacredHandler

# Setup logger - Part #1
setupLogger()

# Check if we have a valid token
if not config.bot_token:
    print('The `bot_token` configuration variable is empty.')
    print('Make sure to configure the bot appropriately prior trying to run it.')
    logger.error("The `bot_token` configuration variable is empty.")
    quit()


# Get Discord Client
client = discord.Client()

# Setup logger - Part #2
addSacredHandler(client)


# Utility function
async def print_role_ids():
    """Utility Function: Print all the roles IDs from all connected servers (guilds)"""
    for g in client.guilds:
        print(g)
        for r in g.roles:
            print('\t' + r.name + ' = ' + str(r.id))


# Setup on_ready() hook
@client.event
async def on_ready():
    login_msg = '[Bot Start] - Logged in as {}#{}'.format(client.user.name, client.user.discriminator)
    print(login_msg)
    logger.info(login_msg)
    await client.change_presence(activity=discord.Game(name='Haven Alpha'))  # tee-hee


# Setup on_message() hook
@client.event
async def on_message(message):
    # Try to use all the registered handlers in the message. If one handles it, break out of the loop
    for handler in message_handlers:
        message_handled = await handler(client, message)
        if message_handled:
            return


# Run the bot!
client.run(config.bot_token)
