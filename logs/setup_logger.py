import logging
from logging.handlers import TimedRotatingFileHandler


def setup_logger(
        file_path,
        name,
        log_to_console_flag=True,
        level=logging.NOTSET,
        formatter="[%(levelname)s] %(asctime)s, %(name)s, line %(lineno)s, %(message)s",
        when="W0",  # once a week (each monday) log will be overwritten
        backup_count=1  # only one file which will be rewritten after
):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = TimedRotatingFileHandler(filename=file_path,
                                  backupCount=backup_count,
                                  when=when)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    if log_to_console_flag:
        logger.addHandler(logging.StreamHandler())
    return logger
