import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

BASE_URL = "https://au.element14.com"
SEARCH_URL = BASE_URL + "/search?st={}"

def scrape(sku: str) -> dict:
    try:
        response = requests.get(SEARCH_URL.format(sku), headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return _fail(sku, f"Search failed with status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        product_link = soup.select_one("a.productListerName")

        if not product_link:
            return _fail(sku, "No product link found")

        product_url = BASE_URL + product_link["href"]
        product_response = requests.get(product_url, headers=HEADERS, timeout=10)
        if product_response.status_code != 200:
            return _fail(sku, f"Product page failed with status {product_response.status_code}")

        product_soup = BeautifulSoup(product_response.text, "html.parser")
        price_tag = product_soup.select_one("div.price")

        if not price_tag:
            return _fail(sku, "Price not found")

        raw_price = price_tag.get_text(strip=True).replace("$", "").split("/")[0]
        price = float(raw_price)

        return {
            "supplier": "element14",
            "sku": sku,
            "price": price,
            "currency": "AUD",
            "status": "success"
        }

    except Exception as e:
        return _fail(sku, f"Exception: {str(e)}")

def _fail(sku, reason):
    return {
        "supplier": "element14",
        "sku": sku,
        "price": None,
        "currency": "AUD",
        "status": f"fail: {reason}"
    }
