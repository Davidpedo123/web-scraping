import requests
from bs4 import BeautifulSoup
from config.env import page1_url, page2_url, page3_url
from config.logger import logger

async def consult_page1():
    try:
        r = requests.get(page1_url, verify=False)
        soup = BeautifulSoup(r.content, "html.parser")
        results = soup.find(id="ResultsContainer")
        return soup
    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 1: {e}")
        return None


async def consult_page2():
    try:
        r = requests.get(page2_url, verify=False)
        soup = BeautifulSoup(r.content, "html.parser")

        # Ajusta la clase para cada producto
        products = soup.find_all("div", class_="product-card")  
        products_all = []

        for producto in products:
            nombre = producto.find("div", class_="product-card__titles").get_text(strip=True)
            precio = producto.find("div", attrs={"data-testid": "product-price"}).get_text(strip=True)
            products_all.append({
                "nombre": nombre,
                "precio": precio
            })

        return products_all

    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 2: {e}")
        return None

async def consult_page3():
    try:
        r = requests.get(page3_url,verify=False)
        soup = BeautifulSoup(r.content, "html.parser")
        results = soup.find(id="ResultsContainer")
        return soup
    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 3: {e}")
        return None

