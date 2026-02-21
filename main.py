from src.excel_byer.browser import Browser
from src.excel_byer.parse import Parsing
from trgb import red, yellow
from src.excel_byer.gen_excel import Tables
from src.excel_byer.core import get_url


if __name__ == "__main__":
    try:
        browser = Browser(headless=False)
        browser.start()

        table = Tables()

        url = get_url()

        browser.open(url)

        parser = Parsing(browser.page)

        parser.get_html()
        parser.get_info()

        table.add_row(parser.name, parser.price, 
                      parser.offers["factory_new"], parser.offers["minimal_wear"], 
                      parser.offers["field_tested"], parser.offers["well_worn"], parser.offers["battle_scarred"],
                      link=url
                    )
        table_name = input(yellow("[ script ] Название новой таблицы:"))
        table.save(f"books/{ table_name }.xlsx")

        browser.close()
    except KeyboardInterrupt:
        print("STOPPED")