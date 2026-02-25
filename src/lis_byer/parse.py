from playwright.sync_api import sync_playwright, TimeoutError as err_timeout, Error as err
from trgb import green, yellow, red
from bs4 import BeautifulSoup
import re
from .browser import Browser

class ParsingSite:
    def __init__(self, page):
        self.page = page
        self.browser = Browser()

        self.name = None
        self.price = None
        self.skin_status = None
        self.offers = None

    def get_html(self):
        
        try:
            self.page.wait_for_load_state("domcontentloaded")
            self.html = self.page.content()

            return self.html
        
        except err_timeout:
            self.browser.timeout()
    
    def not_info(self):
        print(red("[ script ] Сайт меня обнаружил. Прошу прощения, но я не могу работать пока на меня смотрят :("))
    
    def get_info(self, url):
        
        soup = BeautifulSoup(self.html, "html.parser")
        print(yellow(f"[ script ] Анализ: {url}"))
    
        skin_name = soup.find("div", class_="skin-name")
        min_price = soup.find("div", class_="min-price-value")
        status = soup.select_one(
            "div.unhold-date, div.delayed-delivery, div.instant-delivery"
        )

        status_text = ""

        if skin_name and min_price and status:

            self.name = skin_name.get_text(strip=True)
            print(green(f"[ script ] {skin_name}"))

            self.price = str(min_price.contents[0]).strip()
            print(green(f"[ script ] {min_price}"))

            status_text = status.find("span", class_=False)
        else:
            self.not_info()
        
        if status_text:
            if "Разблокирован" in status_text.get_text(strip=True):
                self.skin_status = "Разблокирован"
            else:
                self.skin_status = status_text.get_text(strip=True)
                
        self.offers = {
            "FN": 0,
            "MW": 0,
            "FT": 0,
            "WW": 0,
            "BS": 0,
        }

        for block in soup.select(".skins-market-exterior"):
            offers_title = block.select_one(".skins-market-wear-title")
            desc = block.select_one(".skins-market-wear-description")
        
            if not desc or not offers_title:
                continue

            offers_text = desc.get_text(strip=True)

            self.count = re.search(r"\d+", offers_text)

            self.offers_count = int(self.count.group()) if self.count else 0

            if "Прямо с завода" in offers_title.get_text(strip=True):
                self.offers["FN"] = self.offers_count
            elif "Немного поношенное" in offers_title.get_text(strip=True):
                self.offers["MW"] = self.offers_count
            elif "После полевых испытаний" in offers_title.get_text(strip=True):
                self.offers["FT"] = self.offers_count
            elif "Поношенное" in offers_title.get_text(strip=True):
                self.offers["WW"] = self.offers_count
            elif "Закалённое в боях" in offers_title.get_text(strip=True):
                self.offers["BS"] = self.offers_count

            print(green(f"[ script ] {offers_title}"))


        