from src.lis_byer.browser import Browser
from src.lis_byer.parse import ParsingSite
from trgb import yellow, red, green
from src.lis_byer.gen_excel import Tables
from pathlib import Path
import os, sys

class Main:

    def main(self):

        if getattr(sys, "frozen", False):
            base_dir = Path(sys.executable).parent
            browsers_dir = base_dir / "_internal" / "browsers"
        else:
            base_dir = Path(__file__).resolve().parent
            browsers_dir = base_dir / "browsers"
        

        books_dir = base_dir / "books"
        data_dir = base_dir / "data"

        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(browsers_dir)

        books_dir.mkdir(exist_ok=True)
        data_dir.mkdir(exist_ok=True)

        file_path = data_dir / "data.txt"

        if not file_path.exists():
            file_path.touch()
            print(red("[ script ] Файл data.txt не был обнаружен. Файл был создан, добавьте ссылки и сделайте перезапуск."))
            input()
            sys.exit(2)

        table = Tables()
        
        with open(file_path, "r", encoding="utf-8") as file:
            if file_path.stat().st_size == 0:
                print(red("[ script ] Файл пустой. Добавьте ссылки..."))
                input()
                sys.exit(1)

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
                        parser.offers["FT"], parser.offers["WW"], 
                        parser.offers["BS"], all_offers=parser.all_offers,
                        skin_status=parser.skin_status, link=url
                        )
                
                browser.close()
                
        table_name = input(yellow("[ script ] Название новой таблицы: "))
        table.save(f"books/{ table_name }.xlsx")
        input()

if __name__ == "__main__":
    sesion = Main()

    sesion.main()
