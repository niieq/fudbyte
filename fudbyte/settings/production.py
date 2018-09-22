from .base import *

DEBUG = False


ALLOWED_HOSTS = ['23.239.3.11', 'fudbyte.com', 'www.fudbyte.com', '*.fudbyte.com']

BROKER_URL = os.environ.setdefault('BROKER_URL', '')


try:
	from .local import *
except ImportError:
	pass
