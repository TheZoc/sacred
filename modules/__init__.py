import logging
logger = logging.getLogger('sacred')

from modules.logger_module import setupLogger, addSacredHandler
from modules.welcome_channel import welcome_channel_handler
from modules.sfc_pugs import sfc_pug_handler

message_handlers = []

message_handlers.append(welcome_channel_handler)
message_handlers.append(sfc_pug_handler)
