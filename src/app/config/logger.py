import logging
from logging.handlers import RotatingFileHandler
import os
import sys

main_path = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
log_dir = os.path.join(main_path, "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'cliente_http.log')

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
file_handler = RotatingFileHandler(log_file, maxBytes=1_000_000, backupCount=5)
file_handler.setFormatter(formatter)

logger = logging.getLogger("cliente_http")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

