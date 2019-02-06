import logging
logger = logging.getLogger('sacred')

from modules.logger_module import setupLogger, addSacredHandler
from modules.welcome_channel import welcome_channel_handler
from modules.sfc_pugs import sfc_pugs_handler, sfc_pugs_task

message_handlers = []
background_tasks = []

message_handlers.append(welcome_channel_handler)
message_handlers.append(sfc_pugs_handler)

background_tasks.append(sfc_pugs_task)
