#!/usr/local/bin/python3.5

import discord
import asyncio
import datetime
import bot_config

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
        print('[' + message.timestamp.strftime('%Y-%m-%d %H:%M:%S') + ']', end=' ')
        print('User ' + message.author.name + '#' + message.author.discriminator, end=' ')
        print('has accepted the terms.')

        try:
            member_role = discord.utils.get(message.server.roles, id=bot_config.get_member_role_id())
            await client.add_roles(message.author, member_role)

        except discord.Forbidden:
            print(">>> I lack the permissions to add the role the user.")
            return

        except discord.HTTPException:
            print(">>> HTTPException (?!)")
            return

        try:
            await client.delete_message(message)

        except discord.Forbidden:
            print(">>> I lack the permissions to add the role the user.")
            return

        except discord.HTTPException:
            print(">>> HTTPException (?!)")
            return

async def delete_unwanted_welcome_messages(message):
    if (bot_config.get_welcome_channel_id() == message.channel.id):
        if (message.author.id not in bot_config.roles_allowed_to_msg_welcome_channel()):
            try:
                await client.delete_message(message)
    
            except discord.Forbidden:
                print(">>> I lack the permissions to add the role the user.")
                return

            except discord.HTTPException:
                print(">>> HTTPException (?!)")
                return 

@client.event
async def on_ready():
    print('Logged in as', end=' ')
    print(client.user.name + "#" + client.user.discriminator)

@client.event
async def on_message(message):
    if message.content.startswith('!accept'):
        await user_accepted_terms(message)
    else:
        await delete_unwanted_welcome_messages(message)

client.run(bot_config.get_bot_token())

