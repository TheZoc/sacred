'''
This file handles the messages `!pugme` and `!unpugme`
and add the messenger to the pug group.
'''

import discord
import bot_config as config
from modules import logger
import datetime
import json
import aiofiles
import asyncio

puggers = {}


async def sfc_pugs_handler(client, message):
    '''
    Handles the !pugme and !unpugme messages
    '''
    if (message.channel.id not in config.sfcpugger_allowed_channels):
        return False

    pugme = message.content.startswith('!pugme')
    unpugme = message.content.startswith('!unpugme')

    # Only parse !pugme and !unpugme messages
    if not pugme and not unpugme:
        return False

    result = False
    if pugme:
        result = add_pugger(client, message.author, 'User asked to be added to the SourceForts Classic pug group')
    else:
        result = remove_pugger(client, message.author, 'User asked to be removed from the SourceForts Classic pug group')

    # Only write to disk if any change happened
    if result:
        await dump_dict(puggers)

    return result


async def dump_dict(pugdict):
    '''
    Writes down the pugger list to disk.
    TODO: Avoid spamming the disk! Set limits!
    TODO: Make non-blocking write calls
    '''
    async with aiofiles.open(config.sfcpugger_mem_path, 'w') as file:
        try:
            await file.write(json.dumps(pugdict))
            logmsg = 'Saved pugger checkins to disk'
            print(logmsg)
            logger.info(logmsg)
        except Exception as ex:
            logmsg = 'Exception: {}\n'.format(str(ex))
            logmsg += 'Could not write to json from {0}'.format(config.sfcpugger_mem_path)
            print(logmsg)
            logger.info(logmsg)


async def sfc_pugs_task(client):
    '''
    Background task to check for pugger status timeouts
    '''
    global puggers

    await client.wait_until_ready()

    while not client.is_closed():
        try:
            async with aiofiles.open(config.sfcpugger_mem_path, 'r') as f:
                try:
                    pd = json.loads(await f.read())
                    puggers = {**puggers, **{int(k): v for k, v in pd.items()}}
                except Exception as ex:
                    logmsg = 'Exception: {}\n'.format(str(ex))
                    logmsg += 'Could not write to json from {0}'.format(config.sfcpugger_mem_path)
                    print(logmsg)
                    logger.info(logmsg)

            for k, v in puggers.items():
                time_diff = (datetime.datetime.now() - datetime.datetime.strptime(v['ts'], "%Y-%m-%d %H:%M"))

                if time_diff.seconds >= (config.sfcpugger_timeout * 60):
                    reason = 'Automatically restored from cached state'
                    guild = client.get_guild(id=v['g'])
                    user = guild.get_member(k)
                    await remove_pugger(client, user, reason)

        except FileNotFoundError:
            logmsg = 'File Not Found while attempting to read cache file at: {}\n'.format(config.sfcpugger_mem_path)
            print(logmsg)
            logger.info(logmsg)
        finally:
            await asyncio.sleep(config.sfcpugger_interval * 60)


async def add_pugger(client, user, reason='No reason set'):
    '''Add the user to the specified role'''

    # Skiping logs for now
#    logMessage = '[!pugme]' + \
#        ' User ' + message.author.name + '#' + message.author.discriminator + \
#        ' asked to be a pugger.'
#    logger.info(logMessage)

    # Set the user role. If not possible, log it.
    try:
        pugger_role = discord.utils.get(user.guild.roles, id=config.sfcpugger_role_id)
        await user.add_roles(pugger_role, reason=reason)
        puggers[user.id] = {'g': user.guild.id, 'ts': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}

    except discord.Forbidden:
        logmsg = '[!pugme] Insufficient permission to add the specified role to the user.'
        print(logmsg)
        logger.error(logmsg)

    except discord.HTTPException:
        logmsg = '[!pugme] HTTPException (?!)'
        print(logmsg)
        logger.error(logmsg)

    # Message handled
    return True


async def remove_pugger(client, user, reason='No reason set'):
    '''Add the user to the specified role'''

    # Skiping logs for now
#    logMessage = '[!pugme]' + \
#        ' User ' + message.author.name + '#' + message.author.discriminator + \
#        ' asked to be a pugger.'
#    logger.info(logMessage)

    # Set the user role. If not possible, log it.
    try:
        pugger_role = discord.utils.get(user.guild.roles, id=config.sfcpugger_role_id)
        await user.remove_roles(pugger_role, reason=reason)

        try:
            del puggers[user.id]
        except KeyError:
            pass

    except discord.Forbidden:
        logmsg = '[!pugme] Insufficient permission to remove the specified role from the user.'
        print(logmsg)
        logger.error(logmsg)

    except discord.HTTPException:
        logmsg = '[!pugme] HTTPException (?!)'
        print(logmsg)
        logger.error(logmsg)

    # Message handled
    return True
