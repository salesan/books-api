import logging
import sys
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

log_handler = logging.StreamHandler(sys.stdout)
formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d"
)
log_handler.setFormatter(formatter)

logger.addHandler(log_handler)
