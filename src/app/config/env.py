from dotenv import load_dotenv
from config.logger import logger
import os

load_dotenv('C:/Users/etejada/OneDrive - INAFOCAM/Documentos/Personal/web-scraping/.env')


page1_url = os.environ.get('PAGE1_URL')
page2_url = os.environ.get('PAGE2_URL')
page3_url = os.environ.get('PAGE3_URL')


logger.info(f"Loaded URLs from .env: {page1_url}, {page2_url}, {page3_url}")