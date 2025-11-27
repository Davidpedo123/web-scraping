from dotenv import load_dotenv
from config.logger import logger
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
ENV_PATH = os.path.join(BASE_DIR, 'env')


load_dotenv(ENV_PATH)

page1_url = os.environ.get('PAGE1_URL')
page2_url = os.environ.get('PAGE2_URL')
page3_url = os.environ.get('PAGE3_URL')


logger.info(f"Loaded URLs from .env: {page1_url}, {page2_url}, {page3_url}")