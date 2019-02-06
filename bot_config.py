#!/usr/bin/python

# Discord bot token
try:
	bot_token = open('token', 'r').read()
except:
	bot_token = ''

#cleans up bot commands in chat
hide_cmds = True

#displays extra info at init
verbose_start = True

# #welcome channel ID (Where the bot will look for the !accept command)
welcome_channel_id = 0

# Member role ID
member_role_id = 0

# SourceForts Classic Puggers
sfcpugger_role_id = 0

#Time to wait before pugger status is removed (in minutes)
sfcpugger_timeout = 180

#time to wait before checking pugger status timeouts (in minutes)
sfcpugger_interval = 10

#filepath that keeps track of pug status checkins
sfcpugger_mem_path = 'modules/sfcpugger_state'

# Channels that the !pugme and !unpugme commands will be allowed
sfcpugger_allowed_channels = {}

# Roles with permission to send messages in #welcome channel
welcome_allowed_roles_msg = {}
