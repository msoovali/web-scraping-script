import bs4
import datetime
import urllib.request
from bs4 import BeautifulSoup as soup

URL_FILE = "URLS"
PRICES = "PRICES"

def getProductName(product_url):
    return product_url.split('/')[-1]

def saveProductAsHTML(product_url, product_name):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(product_url, f"./scraped_pages/{product_name}")
    
def scrapeProductPrice(product_name):    
    with open(f"./scraped_pages/{product_name}", 'r') as f:
        html = f.read()

    page_soup = soup(html, "html.parser")

    price = page_soup.findAll("div", {"class":"price-holder"})[0].div["data-sell-price-w-vat"]
    with open(PRICES, 'a') as f:
        f.write(f"{product_name};{price}\n")
    return float(price)

if __name__ == "__main__":
    with open(URL_FILE) as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]
    total = 0
    with open(PRICES, 'a') as f:
        f.write(f"{5*'*'}{datetime.datetime.now()}{5*'*'}\n")
    for url in urls:
        product_name = getProductName(url)
        saveProductAsHTML(url, product_name)
        total += scrapeProductPrice(product_name)
    with open(PRICES, 'a') as f:
        f.write(f"{5*'*'} Total: {int(total)}€ {5*'*'}\n\n")