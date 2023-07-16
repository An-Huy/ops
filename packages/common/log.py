import logging
from logging.handlers import TimedRotatingFileHandler
from packages.common import conf as cfg

CONF = cfg.CONF

MAP_LOGLEVEL = {'debug': logging.DEBUG,
                'warning': logging.WARNING,
                'info': logging.INFO,
                'critical': logging.CRITICAL,
                'error': logging.ERROR}

def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(MAP_LOGLEVEL[CONF['logging']['log_level']])

    # create the logging file handler
    FILEPATH = CONF['logging']['log_folder'] + 'multiapi.log'
    fh = TimedRotatingFileHandler(FILEPATH, when='D', backupCount=10)
    formatter = logging.Formatter('%(asctime)s -'
                                  ' %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger

if __name__ == "__main__":
    LOG = getLogger(__name__)
    LOG.info("Welcome to  Logging")
    LOG.debug("A debugging message")
    LOG.warning("A warning occurred")
    LOG.error("An error occurred")
    LOG.exception("An Exception occurred")