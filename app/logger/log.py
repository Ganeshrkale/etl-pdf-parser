import logging
import sys
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
logger.propagate = False
logger.setLevel(logging.DEBUG)
logHandler = logging.StreamHandler(sys.stderr)
logging.addLevelName(logging.ERROR, 'error')
logging.addLevelName(logging.WARNING, 'warning')
logging.addLevelName(logging.INFO, 'info')
logging.addLevelName(logging.DEBUG, 'debug')
formatter = jsonlogger.JsonFormatter('%(asctime)s - %(levelname)s - %(api)s - %(user)s - %(message)s - %(ParserType)s - %(DistributorCode)s -  %(ProcessTime)s - %(RequstType)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)