import discord

# Utility function
async def print_role_ids(client):
    """Utility Function: Print all the roles IDs from all connected servers (guilds)"""
    for g in client.guilds:
        print('  %s' % g)
        for r in g.roles:
            print('    ' + r.name + ' = ' + str(r.id))

async def print_all_chans(client):
    text_channel_list = []
    voice_channel_list = []
    for server in client.guilds:
        print('Server tree:')
        print(' >%s %d' % (server.name, server.id))

        print(' |->%s' % 'Category Channels')
        for channel in server.channels:
            if type(channel) == discord.channel.CategoryChannel:
                print(' |  |->%s %d' % (channel.name, channel.id))
                voice_channel_list.append(channel)

        print(' |->%s' % 'Text Channels')
        for channel in server.channels:
            if type(channel) == discord.channel.TextChannel:
                print(' |  |->%s %d' % (channel.name, channel.id))
                text_channel_list.append(channel)

        print(' |->%s' % 'Voice Channels')
        for channel in server.channels:
            if type(channel) == discord.channel.VoiceChannel:
                print(' |  |->%s %d' % (channel.name, channel.id))
                voice_channel_list.append(channel)