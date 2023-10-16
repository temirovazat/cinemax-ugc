import logging
from logging import config as logging_config
from secrets import token_hex
from typing import Optional

from core.config import CONFIG


class RequestIdFilter(logging.Filter):
    """A class for an additional log message filter to add request ID information to them."""

    def __init__(self, request_id: Optional[str]):
        """Initialize the class with an expected request ID.

        Args:
            request_id: Unique request identifier
        """
        self.request_id = request_id or token_hex(16)

    def filter(self, record: logging.LogRecord) -> bool:
        """Add information to the log in the main method.

        Args:
            record: The record being processed

        Returns:
            bool: A non-zero value for recording the entry
        """
        record.request_id = self.request_id
        return True


LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
        },
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': '%(levelprefix)s %(message)s',
            'use_colors': None,
        },
        'access': {
            '()': 'uvicorn.logging.AccessFormatter',
            'fmt': "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'access': {
            'formatter': 'access',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'logstash': {
            'class': 'logstash.LogstashHandler',
            'level': 'INFO',
            'host': CONFIG.logstash.host,
            'port': CONFIG.logstash.port,
        },
    },
    'loggers': {
        'app': {
            'handlers': ['logstash', 'console'],
            'level': 'INFO',
        },
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['logstash'],
        },
        'uvicorn.access': {
            'handlers': ['access', 'logstash'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'level': 'INFO',
        'formatter': 'verbose',
        'handlers': LOG_DEFAULT_HANDLERS,
    },
}

logging_config.dictConfig(LOGGING)
