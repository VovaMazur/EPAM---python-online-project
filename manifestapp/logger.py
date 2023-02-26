"""Logger setup module"""
import logging
# from flask import current_app as app


def logger_setup(callfrom, msg, filename, level):
    """Logger setup function for the application """

    logger = logging.getLogger(callfrom)
    formatter = logging.Formatter(msg, datefmt='%m/%d/%Y %I:%M:%S %p')

    # with app.app_context():
    #     print('Inside app context')
    #fullfilename = os.path.join(Path(app.root_path).parent, filename)

    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    strm_handler = logging.StreamHandler()
    strm_handler.setFormatter(formatter)

    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(strm_handler)

    return logger
