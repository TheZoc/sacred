import logging
import logging.handlers

'''
This module logs any messages to the specified file.
Right now it's pretty basic and a complete rework must be done.
'''

# Setup logging. Very hackish for now, but I don't want to delay the discord announcement anymore.
# TODO: Create a class for async log handling
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
maxLogSize = 20 * 1024 * 1024
logBackupAmount = 20
logName = 'discord.log'
handler = logging.handlers.RotatingFileHandler(filename=logName, encoding='UTF-8', maxBytes=maxLogSize, backupCount=logBackupAmount)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
