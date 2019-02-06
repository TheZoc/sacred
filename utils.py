import discord


# Utility function
async def get_all_role_ids(client):
    '''
    Utility Function: Print all the roles IDs from all connected servers (guilds)
    '''
    return_msg = 'Roles:\n'
    for g in client.guilds:
        return_msg += '  {}\n'.format(str(g))
        for r in g.roles:
            return_msg += '    {} = {}\n'.format(r.name, str(r.id))

    return return_msg


def get_all_channels(client):
    '''
    Utility Function: Gets all the text and voice channels
    '''
    text_channel_list = []
    voice_channel_list = []
    return_msg = ''
    for server in client.guilds:
        return_msg += 'Server tree: >{} [{}]\n'.format(server.name, server.id)

        return_msg += ' |->Category Channels\n'
        for channel in server.channels:
            if type(channel) == discord.channel.CategoryChannel:
                return_msg += ' |  |->{} {}\n'.format(channel.name, channel.id)
                voice_channel_list.append(channel)

        return_msg += ' |->Text Channels\n'
        for channel in server.channels:
            if type(channel) == discord.channel.TextChannel:
                return_msg += ' |  |->{} {}\n'.format(channel.name, channel.id)
                text_channel_list.append(channel)

        return_msg += ' |->Voice Channels\n'
        for channel in server.channels:
            if type(channel) == discord.channel.VoiceChannel:
                return_msg += ' |  |->{} {}\n'.format(channel.name, channel.id)
                voice_channel_list.append(channel)

    return return_msg
