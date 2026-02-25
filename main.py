from src.lis_byer.browser import Browser
from src.lis_byer.parse import ParsingSite
from trgb import yellow
from src.lis_byer.gen_excel import Tables
from pathlib import Path

class Main:

    def main(self):

        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / "data" / "data.txt"

        table = Tables()
        
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                url = str(line)

                browser  = Browser(headless=True)

                browser.start()
                browser.open(url)

                parser = ParsingSite(browser.page)

                parser.get_html()
                parser.get_info(url)


                if parser.offers:
                    table.add_row(parser.name, parser.price, 
                        parser.offers["FN"], parser.offers["MW"], 
                        parser.offers["FT"], parser.offers["WW"], parser.offers["BS"], skin_status=parser.skin_status,
                        link=url
                        )
                
                browser.close()
                
        table_name = input(yellow("[ script ] Название новой таблицы: "))
        table.save(f"books/{ table_name }.xlsx")

if __name__ == "__main__":
    sesion = Main()

    sesion.main()
