import logging
from colorlog import ColoredFormatter

GSDCON_LEVEL = 35
GSDPROD_LEVEL = 25
MILESTONE_LEVEL = 45

logging.addLevelName(GSDCON_LEVEL, "GSDCON")
logging.addLevelName(GSDPROD_LEVEL, "GSDPROD")
logging.addLevelName(MILESTONE_LEVEL, "MILESTONE")

def gsdcon(self, message, *args, **kws):
    self._log(GSDCON_LEVEL, message, args, **kws)

def gsdprod(self, message, *args, **kws):
    self._log(GSDPROD_LEVEL, message, args, **kws)

def milestone(self, message, *args, **kws):
    self._log(MILESTONE_LEVEL, message, args, **kws)

logging.Logger.gsd_consumer = gsdcon
logging.Logger.gsd_producer = gsdprod
logging.Logger.milestone = milestone

def init_logger():
    # Configure logging
    logger = logging.getLogger()
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    formatter = ColoredFormatter(
        "%(log_color)s[%(levelname)s-%(process)d]%(reset)s %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO': 'magenta',
            'GSDPROD': 'green',
            'GSDCON': 'red',
            'MILESTONE': 'blue',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )

    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


# import logging
# from termcolor import colored

# class ColoredFormatter(logging.Formatter):
#     COLORS = {
#         'WARNING': 'yellow',
#         'INFO': 'magenta',
#         'CONSUMER': 'green',
#         'PRODUCER': 'blue',
#         'DEBUG': 'orange',
#         'CRITICAL': 'red',
#         'ERROR': 'red'
#     }

#     def format(self, record):
#         log_message = super().format(record)
#         return colored(log_message, self.COLORS.get(record.levelname))

# def init_logger(role="INFO"):
#     logger = logging.getLogger()
#     logger.setLevel(logging.INFO)

#     ch = logging.StreamHandler()
#     formatter = ColoredFormatter(f"%(asctime)s - {role} - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
#     ch.setFormatter(formatter)
#     logger.addHandler(ch)
#     return logger
