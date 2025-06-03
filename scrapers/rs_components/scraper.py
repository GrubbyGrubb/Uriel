import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

BASE_URL = "https://au.rs-online.com"
SEARCH_URL = BASE_URL + "/web/c/?searchTerm={}"

def scrape(sku: str) -> dict:
    try:
        response = requests.get(SEARCH_URL.format(sku), headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return _fail(sku, f"Search failed with status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        link_tag = soup.select_one("a.productListLink")
        if not link_tag:
            return _fail(sku, "No product link found")

        product_url = BASE_URL + link_tag["href"]
        product_response = requests.get(product_url, headers=HEADERS, timeout=10)
        if product_response.status_code != 200:
            return _fail(sku, f"Product page failed with status {product_response.status_code}")

        product_soup = BeautifulSoup(product_response.text, "html.parser")
        price_tag = product_soup.select_one(".price .rs-price")
        if not price_tag:
            return _fail(sku, "Price not found")

        raw_price = price_tag.get_text(strip=True).replace("$", "").split(" ")[0]
        price = float(raw_price)

        return {
            "supplier": "rs_components",
            "sku": sku,
            "price": price,
            "currency": "AUD",
            "status": "success"
        }

    except Exception as e:
        return _fail(sku, f"Exception: {str(e)}")

def _fail(sku, reason):
    return {
        "supplier": "rs_components",
        "sku": sku,
        "price": None,
        "currency": "AUD",
        "status": f"fail: {reason}"
    }
