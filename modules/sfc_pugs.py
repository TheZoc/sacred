'''
This file handles the messages `!pugme` and `!unpugme`
and add the messenger to the pug group.
'''

import discord
import bot_config as config
from modules.logger import logger
import datetime
from datetime import timedelta
import json
import aiofiles
import asyncio

puggers = {}

async def sfc_pugs_handler(client, message):
    '''Handles the messages sent in the #welcome channel'''
    if (message.channel.id not in config.sfcpugger_allowed_channels):
        return False

    if message.content.startswith('!pugme'):
        f = add_pugger
        reason = 'User asked to be added to the SourceForts Classic pug group'
    elif message.content.startswith('!unpugme'):
        f = remove_pugger
        reason = 'User asked to be removed from the SourceForts Classic pug group'

    result = await f(client, message.author, reason)
    await dump_dict(puggers)
    return result


async def dump_dict(pugdict):
    async with aiofiles.open(config.sfcpugger_mem_path, 'w') as f:
        try:
            await f.write(json.dumps(pugdict))
            logger.info('Saved pugger checkins to disk')
        except Exception as ex:
            print(ex)
            print('Could not write to json from {0}'.format(config.sfcpugger_mem_path))


async def sfc_pugs_task(client):
    '''background task to check for pugger status timeouts'''
    global puggers

    await client.wait_until_ready()

    while not client.is_closed():
        try:
            async with aiofiles.open(config.sfcpugger_mem_path, 'r') as f:
                try:
                    pd = json.loads(await f.read())
                    puggers = {**puggers, **{int(k):v for k,v in pd.items()}}
                except Exception as ex:
                    print(ex)
                    print('Could not load valid json from {0}'.format(config.sfcpugger_mem_path))

            for k, v in puggers.items():
                time_diff = (datetime.datetime.now() - datetime.datetime.strptime(v['ts'], "%Y-%m-%d %H:%M"))
                
                if time_diff.seconds >= (config.sfcpugger_timeout * 60):
                    reason='Automatically restored from cached state'
                    guild = client.get_guild(id=v['g'])
                    user = guild.get_member(k)
                    await remove_pugger(client, user, reason)
            print('                               ')

        except FileNotFoundError:
            print('Error reading cache file at %s' % config.sfcpugger_mem_path)
        finally:
            await asyncio.sleep((config.sfcpugger_interval * 60))


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
        puggers[user.id] = {'g': user.guild.id, 'ts':datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
    
    except discord.Forbidden:
        logger.error('[!pugme] Insufficient permission to add the specified role to the user.')

    except discord.HTTPException:
        logger.error("[!pugme] HTTPException (?!)")

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
            del(puggers[message.author.id])
        except:
            pass

    except discord.Forbidden:
        logger.error('[!pugme] Insufficient permission to remove the specified role from the user.')

    except discord.HTTPException:
        logger.error("[!pugme] HTTPException (?!)")

    # Message handled
    return True


