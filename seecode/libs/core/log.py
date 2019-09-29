# coding:utf-8

import logging
import sys

logger = logging.getLogger(__name__)

try:
    from seecode.libs.core.ansistrm import ColorizingStreamHandler
    LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
except ImportError:
    LOGGER_HANDLER = logging.StreamHandler(sys.stdout)

FORMATTER_INFO = logging.Formatter("\r[%(asctime)s] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
FORMATTER_DEV = logging.Formatter("\r[%(asctime)s] [%(pathname)s(%(lineno)d)%(funcName)s()] [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
LOGGER_HANDLER.setFormatter(FORMATTER_DEV)
LOGGER_HANDLER.setFormatter(FORMATTER_INFO)

logger.addHandler(LOGGER_HANDLER)
logger.setLevel(logging.DEBUG)
