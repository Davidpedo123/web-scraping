import requests
from bs4 import BeautifulSoup
from config.env import page1_url, page2_url, page3_url
from config.logger import logger
import os

async def consult_page1():
    try:
        r = requests.get(page1_url, verify=False)
        logger.info(f"[{__name__}] page1 status: {r.status_code}")

        if r.status_code != 200:
            logger.error(f"[{__name__}] Failed to retrieve page: {r.status_code}")
            return None

        

        soup = BeautifulSoup(r.content, "html.parser")
        products = soup.find_all("div", class_="product details product-item-details")  
        logger.info(f"[{__name__}] Number of products found on page 1: {len(products)}")
        products_all = []

        for producto in products:
            nombre = producto.find("a", class_="product-item-link").get_text(strip=True)
            precio = producto.find("span", class_="price").get_text(strip=True)
            products_all.append({
                "nombre": nombre,
                "precio": precio
            })

        logger.info(f"[{__name__}] Successfully consulted page 1")
        #logger.info(f"[{__name__}] Products found on page 1: {products_all}")
        return products_all
    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 1: {e}")
        return None


async def consult_page2():
    try:
        r = requests.get(page2_url, verify=False)
        soup = BeautifulSoup(r.content, "html.parser")

      
        products = soup.find_all("div", class_="product-card")  
        products_all = []
        logger.info(f"[{__name__}] Number of products found on page 2: {len(products)}")
        for producto in products:
            nombre = producto.find("div", class_="product-card__titles").get_text(strip=True)
            precio = producto.find("div", attrs={"data-testid": "product-price"}).get_text(strip=True)
            products_all.append({
                "nombre": nombre,
                "precio": precio
            })
        logger.info(f"[{__name__}] Successfully consulted page 2")
        return products_all

    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 2: {e}")
        return None

async def consult_page3():
    try:
        r = requests.get(page3_url, verify=False)
        logger.info(f"[{__name__}] page3 status: {r.status_code}")

        if r.status_code != 200:
            logger.error(f"[{__name__}] Failed to retrieve page: {r.status_code}")
            return None

        

        soup = BeautifulSoup(r.content, "html.parser")
        products = soup.find_all("li", class_="grid__item grid__item--collection-template small--one-half medium-up--one-quarter")  
        logger.info(f"[{__name__}] Number of products found on page 3: {len(products)}")
        products_all = []

        for producto in products:
            nombre = producto.find("div", class_="h4 grid-view-item__title product-card__title").get_text(strip=True)
            precio = producto.find("span", class_="price-item price-item--sale").get_text(strip=True)
            products_all.append({
                "nombre": nombre,
                "precio": precio
            })

        logger.info(f"[{__name__}] Successfully consulted page 3")
        #logger.info(f"[{__name__}] Products found on page 1: {products_all}")
        return products_all
    except Exception as e:
        logger.error(f"[{__name__}] Error consulting page 3: {e}")
        return None
  
