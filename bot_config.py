import os
from dotenv import load_dotenv
load_dotenv()

# Reminder: All of these settings should be added to a `.env` file
# in a KEY=value format instead of modifying this file directly!

# Discord bot token
bot_token = os.getenv("BOT_TOKEN") or ''

# Displays extra info at init
verbose_start = True if (os.getenv('VERBOSE_START') == 'True') else False

# #welcome channel ID (Where the bot will look for the !accept command)
welcome_channel_id = int(os.getenv("WELCOME_CHANNEL_ID") or 0)

# #sacred-logs channel ID (Where the bot will output the logs)
logging_channel = int(os.getenv("LOGGING_CHANNEL") or 0)

# Member role ID
member_role_id = int(os.getenv("MEMBER_ROLE_ID") or 0)

# SourceForts Classic Puggers
sfcpugger_role_id = int(os.getenv("SFCPUGGER_ROLE_ID") or 0)

# Time to wait before pugger status is removed (in minutes)
sfcpugger_timeout = int(os.getenv("SFCPUGGER_TIMEOUT") or 180)

# Time to wait before checking pugger status timeouts (in minutes)
sfcpugger_interval = int(os.getenv("SFCPUGGER_ROLE_ID") or 10)

# Filepath that keeps track of pug status checkins
sfcpugger_mem_path = os.getenv("SFCPUGGER_MEM_PATH") or 'modules/sfcpugger_state'

# Channels that the !pugme and !unpugme commands will be allowed
sfcpugger_allowed_channels = set()

# Roles with permission to send messages in #welcome channel
welcome_msg_allowed_roles = set()


# Populate our sets here
for k, v in os.environ.items():
    # Look for SFCPUGGER_ALLOWED_CHANNEL1, SFCPUGGER_ALLOWED_CHANNEL2, etc.
    if k.startswith('SFCPUGGER_ALLOWED_CHANNEL'):
        sfcpugger_allowed_channels.add(v)

    # Look for WELCOME_MSG_ALLOWED_ROLE1, WELCOME_MSG_ALLOWED_ROLE2, etc.
    elif k.startswith('WELCOME_MSG_ALLOWED_ROLE'):
        welcome_msg_allowed_roles.add(v)
