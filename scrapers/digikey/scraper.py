import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0",
}

BASE_URL = "https://www.digikey.com.au"
SEARCH_URL = BASE_URL + "/en/products/result?keywords={}"

def scrape(sku: str) -> dict:
    try:
        response = requests.get(SEARCH_URL.format(sku), headers=HEADERS, timeout=10)
        if response.status_code != 200:
            return _fail(sku, f"Search failed with status {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        link_tag = soup.select_one("a.part-link")
        if not link_tag:
            return _fail(sku, "No product link found")

        product_url = BASE_URL + link_tag["href"]
        product_response = requests.get(product_url, headers=HEADERS, timeout=10)
        if product_response.status_code != 200:
            return _fail(sku, f"Product page failed with status {product_response.status_code}")

        product_soup = BeautifulSoup(product_response.text, "html.parser")
        price_cell = product_soup.select_one("tr.tr-price-break td:nth-of-type(2)")
        if not price_cell:
            return _fail(sku, "Price cell not found")

        raw_price = price_cell.get_text(strip=True).replace("$", "").split(" ")[0]
        price = float(raw_price)

        return {
            "supplier": "digikey",
            "sku": sku,
            "price": price,
            "currency": "AUD",
            "status": "success"
        }

    except Exception as e:
        return _fail(sku, f"Exception: {str(e)}")

def _fail(sku, reason):
    return {
        "supplier": "digikey",
        "sku": sku,
        "price": None,
        "currency": "AUD",
        "status": f"fail: {reason}"
    }
