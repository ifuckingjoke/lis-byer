from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as timeout
from trgb import green, yellow, red

class Browser:
    def __init__(self, user_data_dir="lis_skins/user_data", headless=False):
        self.user_data = user_data_dir
        self.headless = headless
        self.playwright = None
        self.context = None
        self.page = None
    
    def start(self):
        self.playwright = sync_playwright().start()
        
    #    iphone = self.playwright.devices["iPhone 13"]

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data,
            headless = self.headless,
            locale="ru-RU"
        )

        self.page = self.context.new_page()

       # self.page.on("response", lambda r: print(r.url))
    
#    def is_logged(self):

  #      url = self.page.url.lower()

  #      if "login" in url or "passport" in url:

#            print(yellow("[ script ] Для работы скрипта требуется авторизация"))
 #           input(green("[ script ] Для продолжения нажмите Enter..."))

#           self.page.reload()
            
#            return False

 #       return True
    
    def open(self, url):
        try:
            self.page.goto(url)
            self.page.wait_for_load_state("domcontentloaded")
        except timeout:
            print(red("[ script ] Нет ответа от сервера. Возможно произошла переадресация на защиту."))
    
    def close(self):
        self.context.close() 
        self.playwright.stop()