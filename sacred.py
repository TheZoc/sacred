#!/usr/local/bin/python3
import discord
import bot_config as config
from modules import message_handlers, logger


# Check if we have a valid token
if not config.bot_token:
    print('The `bot_token` configuration variable is empty.')
    print('Make sure to configure the bot appropriately prior trying to run it.')
    logger.error("The `bot_token` configuration variable is empty.")
    quit()


# Get Discord Client
client = discord.Client()


# Utility function
async def print_role_ids():
    """Utility Function: Print all the roles IDs from all connected servers"""
    for s in client.servers:
        print(s)
        for r in s.roles:
            print('\t' + r.name + ' = ' + r.id)


# Setup on_ready() hook
@client.event
async def on_ready():
    print('Logged in as', end=' ')
    print(client.user.name + "#" + client.user.discriminator)
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
