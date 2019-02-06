#!/usr/local/bin/python3
import discord
import bot_config as config
from modules import message_handlers, logger, setupLogger, addSacredHandler, background_tasks
import utils

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


# Setup on_ready() hook
@client.event
async def on_ready():
    login_msg = '[Bot Start] - Logged in as {}#{}'.format(client.user.name, client.user.discriminator)

    if config.verbose_start:
        login_msg += utils.get_all_channels(client)
        login_msg += utils.get_all_role_ids(client)

        login_msg += 'Registered message handlers:\n'
        for m in message_handlers:
            login_msg += '  {}'.format(str(m))

        login_msg += 'Registered background tasks:\n'
        for b in background_tasks:
            login_msg += '  {}'.format(str(b))

    # Log what we currently have
    print(login_msg)
    logger.info(login_msg)

    # Init background tasks
    for b in background_tasks:
        client.loop.create_task(b(client))

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
