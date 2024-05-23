from logging import getLogger

logger = getLogger("langStory")


def get_logger(name: str):
    return logger.getChild(name)
