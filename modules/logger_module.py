import logging
import logging.handlers
import bot_config as config
import asyncio


class SacredHandler(logging.Handler):
    def __init__(self, discord_client):
        logging.Handler.__init__(self)  # run parent __init__ class
        self.client = discord_client

    def emit(self, record):
        try:
            msg = self.format(record)

            # asyncio.get_running_loop() is only available on Python 3.7+
            # This makes it compatible with older versions of Python
            loop = self.client.loop

            if loop is not None:
                channel = self.client.get_channel(config.logging_channel)
                loop.create_task(channel.send(msg))
        except RuntimeError:
            # This will happen when exting the bot via Ctrl + C
            pass


def setupLogger(loggerName='sacred',
                defaultLogLevel=logging.INFO,
                fileLogName='sacred.log',
                fileMaxSize=20 * 1024 * 1024,
                fileBackupAmount=20):
    '''
    Sets up a RotatingFileHandler for disk logging
    '''
    logger = logging.getLogger(loggerName)

    # Create a standard formatter
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

    # Create and add RotatingFileHandler
    rfh = logging.handlers.RotatingFileHandler(filename=fileLogName, encoding='UTF-8', maxBytes=fileMaxSize, backupCount=fileBackupAmount)
    rfh.setFormatter(formatter)
    logger.addHandler(rfh)

    # Finally, set the log level
    logger.setLevel(logging.INFO)


def addSacredHandler(discordClient, loggerName='sacred', defaultLogLevel=logging.INFO):
    '''
    Adds a SacredHandler for discord messages logging on the already existing logger.
    This was split from setupLogger() since events can occur before discord connection
    '''
    logger = logging.getLogger(loggerName)

    # Create a standard formatter
    formatter = logging.Formatter('%(levelname)s: %(message)s')

    # Create and add SacredHandler
    sh = SacredHandler(discordClient)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # Finally, set the log level
    logger.setLevel(logging.INFO)
