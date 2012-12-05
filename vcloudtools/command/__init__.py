import logging
from os import environ as env

__all__ = []

_log_level_default = logging.WARN
_log_level = getattr(logging, env.get('VCLOUDTOOLS_LOGLEVEL', '').upper(), _log_level_default)

logging.basicConfig(format='%(levelname)s: %(message)s', level=_log_level)
