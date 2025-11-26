import requests
from bs4 import BeautifulSoup
from config.env import page1_url, page2_url, page3_url
from config.logger import logger

async def consult_page1():
    try:
        r = requests.get(page1_url, verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 1: {e}")
        return None

async def consult_page2():
    try:
        r = requests.get(page2_url, verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 2: {e}")
        return None
    
async def consult_page3():
    try:
        r = requests.get(page3_url,verify=False)
        soup = BeautifulSoup(r.text, 'lxml')
        return soup
    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 3: {e}")
        return None
  
