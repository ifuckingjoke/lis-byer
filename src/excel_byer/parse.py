from playwright.sync_api import sync_playwright, TimeoutError
from trgb import red, green
from bs4 import BeautifulSoup
import re

class Parsing:
    def __init__(self, page):
        self.page = page
        self.timeout_logged = False

    def get_html(self):
        
        try:
            self.page.wait_for_load_state("domcontentloaded")
            self.html = self.page.content()
            return self.html
        
        except TimeoutError:
            print(red("[ script ] нет ответа от сервера. Возможно произошла переадресация на защиту."))
            return False
    
    def get_info(self):
        
        soup = BeautifulSoup(self.html, "html.parser")
        print(green(f"Анализ: {soup.title}"))

        skin_name = soup.find("div", class_="skin-name")

        if skin_name:
            self.name = skin_name.get_text(strip=True)
            print(green(f"{skin_name}"))

        min_price = soup.find("div", class_="min-price-value")

        if min_price:
            self.price = str(min_price.contents[0]).strip()
            print(green(f"{min_price}"))
        
        self.offers = {
            "factory_new": 0,
            "minimal_wear": 0,
            "field_tested": 0,
            "well_worn": 0,
            "battle_scarred": 0,
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
                self.offers["factory_new"] = self.offers_count
            elif "Немного поношенное" in offers_title.get_text(strip=True):
                self.offers["minimal_wear"] = self.offers_count
            elif "После полевых испытаний" in offers_title.get_text(strip=True):
                self.offers["field_tested"] = self.offers_count
            elif "Поношенное" in offers_title.get_text(strip=True):
                self.offers["well_worn"] = self.offers_count
            elif "Закалённое в боях" in offers_title.get_text(strip=True):
                self.offers["battle_scarred"] = self.offers_count

            print(green(f"{offers_title}{self.offers_count}"))




