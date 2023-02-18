import logging


def logger_setup(callfrom, msg, filename, level):
    """Logger setup function for the application """

    logger = logging.getLogger(callfrom)
    formatter = logging.Formatter(msg)
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    strm_handler = logging.StreamHandler()
    strm_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(strm_handler)

    return logger