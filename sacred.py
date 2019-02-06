#!/usr/local/bin/python3
import discord
import bot_config as config
from modules import message_handlers, background_tasks, logger
import utils


# Check if we have a valid token
if not config.bot_token:
    print('The `bot_token` configuration variable is empty.')
    print('Make sure to configure the bot appropriately prior trying to run it.')
    logger.error("The `bot_token` configuration variable is empty.")
    quit()


# Get Discord Client
client = discord.Client()


# Setup on_ready() hook
@client.event
async def on_ready():
    print('Logged in as', end=' ')
    print(client.user.name + "#" + client.user.discriminator)

    if config.verbose_start:
        await utils.print_all_chans(client)
        print('Roles:')
        await utils.print_role_ids(client)
        print('Registered message handlers:')
        for m in message_handlers:
            print('  %s' % str(m))
        print('Registered background tasks:')
        for b in background_tasks:
            print('  %s' % str(b))

    for b in background_tasks:
        client.loop.create_task(b(client))
    print('\nBot active')
    await client.change_presence(activity=discord.Game(name='Haven Alpha'))  # tee-hee


# Setup on_message() hook
@client.event
async def on_message(message):
    # Try to use all the registered handlers in the message. If one handles it, break out of the loop
    for handler in message_handlers:
        message_handled = await handler(client, message)
        if message_handled:
            print('%s | %s: %s' % (message.channel.name, message.author.display_name, message.content))
            if config.hide_cmds:
                await message.delete()
            return


# Run the bot!
client.run(config.bot_token)
