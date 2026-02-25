from playwright.sync_api import sync_playwright, TimeoutError as err_timeout, Error as err
from trgb import red
import time

class Browser:

    def __init__(self, user_data_dir="lis_skins/user_data", headless=False, timeout_count=0):

        self.user_data = user_data_dir
        self.headless = headless
        self.playwright = None
        self.context = None
        self.page = None
        self.timeout_count = timeout_count
    
    def start(self):

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data,
            headless = self.headless,
            locale="ru-RU",
            viewport=None,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
               "AppleWebKit/537.36 (KHTML, like Gecko) "
               "Chrome/121.0.0.0 Safari/537.36"
        )

        self.page = self.context.new_page()
    
    def timeout(self):

        while self.timeout_count < 3:
                print(red("[ script ] Нет ответа от сервера..."))
                print(red("[ script ] Перезагружаю страницу..."))

                self.timeout_count += 1
                self.page.reload()
        else:
            print(red(f"[ script ] Превышено количество попыток {self.timeout_count}."))
            print(red("[ script ] Завершаю работу."))
                
            time.sleep(1)
    
    def not_connect(self):
        print(red("[ script ] Нет подключения к интернету..."))
        time.sleep(2)
    
    def open(self, url):

        try:
            self.page.goto(url, timeout=30000)
            self.page.wait_for_load_state("domcontentloaded")

        except err_timeout:
            self.timeout()
        except err as e:
            if "ERR_INTERNET_DISCONNECTED" in str(e):
                self.not_connect()

    def close(self):
        self.context.close()
        self.playwright.stop()
