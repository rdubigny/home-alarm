import logging
from modules import utils
import config

login_format = '%(asctime)-15s %(message)s'
logging.basicConfig(
    format=login_format,
    level=logging.INFO,
    filename=config.log_path + '/' + utils.get_time() + '.log'
)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.WARNING)
logger = logging.getLogger('tcpserver')
