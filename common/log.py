# encoding:utf-8
from datetime import datetime, timezone, timedelta
import logging
import sys

SWITCH = True


def _get_logger():
    log = logging.getLogger("log")
    log.setLevel(logging.DEBUG)
    console_handle = logging.StreamHandler(sys.stdout)
    console_handle.setFormatter(
        logging.Formatter(
            "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    # file_handle = logging.FileHandler("tmp/log.log", mode="a")
    # file_handle.setFormatter(
    #     logging.Formatter(
    #         "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] - %(message)s",
    #         datefmt="%Y-%m-%d %H:%M:%S",
    #     )
    # )
    log.addHandler(console_handle)
    # log.addHandler(file_handle)
    return log


def debug(arg, *args):
    if len(args) == 0:
        logger.debug(arg)
    else:
        logger.debug(arg.format(*args))


def info(arg, *args):
    if len(args) == 0:
        logger.info(arg)
    else:
        logger.info(arg.format(*args))


def warn(arg, *args):
    if len(args) == 0:
        logger.warning(arg)
    else:
        logger.warning(arg.format(*args))


def error(arg, *args):
    if len(args) == 0:
        logger.error(arg)
    else:
        logger.error(arg.format(*args))


def exception(e):
    logger.exception(e)


# 日志句柄
logger = _get_logger()
logger.info(
    "[System] Service started on: {0}".format(
        datetime.now(timezone(timedelta(hours=8)))
    )
)
