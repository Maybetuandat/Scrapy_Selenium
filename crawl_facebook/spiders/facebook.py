# import scrapy
# from selenium.webdriver.common.by import By
# import time
# import re
# import datetime
# from scrapy_selenium import SeleniumRequest
# from selenium.webdriver.support.ui import WebDriverWait
# from crawl_facebook.items import CrawlFacebookItem, CrawlFacebookReactItem
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver import Chrome
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.support import expected_conditions as EC
# from shutil import which
# class FacebookSpider(scrapy.Spider):
#     name = "facebook"
#     allowed_domains = ["www.facebook.com"]
#     start_urls = ["https://www.facebook.com/",
                    
#                 "https://www.facebook.com/profile.php?id=61560307553960&sk=friends" ,
                    
#                 "https://www.facebook.com/profile.php?id=61560307553960"]
#     scroll_distance = 1080
#     def scroll_down_by(self,driver, distance):
#         driver.execute_script(f"window.scrollBy(0, {distance});")
#     def is_at_bottom(self,driver):
#         return driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight")
#     def __init__(self, *args, **kwargs):
#         super(FacebookSpider, self).__init__(*args, **kwargs)
#         chrome_path = which("chromedriver")
#         chrome_options = ChromeOptions()
#         chrome_options.add_argument("--incognito")
#         # chrome_options.add_argument("--headless")
#         chrome_options.add_argument("--disable-gpu") 
#         chrome_options.add_argument("--window-size=1920,1080")
#         chrome_options.add_argument("--log-level=3")
#         chrome_service = ChromeService(chrome_path)
#         self.driver = Chrome(service=chrome_service, options=chrome_options)
#         self.driver.get(self.start_urls[0])
#         time.sleep(3)   
#         self.driver.implicitly_wait(3)
#         input_account = WebDriverWait(self.driver, 10).until(
#             EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
#         )
#         input_account.send_keys('boxdat123@gmail.com')
#         input_password = self.driver.find_element(By.XPATH, "//input[@id='pass']")
#         input_password.send_keys('123456789aA@')
#         btn_sign = self.driver.find_element(By.XPATH, "//button[@name='login']")
#         btn_sign.click()   
#     def start_requests(self):
#         yield SeleniumRequest(
#             url = self.start_urls[1],
#             wait_time = 3,
#             callback = self.parse_friend,
#             dont_filter=True
#         )
 
#     def parse_friend(self, response):
#         time.sleep(10)
#         # item = CrawlFacebookItem()
#         # index = 1
#         # while not self.is_at_bottom(driver):
#         #     if index == 50: break
#         #     try:
#         #         print("index của select", index)
#         #         friend = driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp'])[{index}]")
#         #         item['name'] = friend.find_element(By.XPATH, ".//div/div/a/span").text
#         #         item['idUser'] = friend.find_element(By.XPATH, ".//div/a").get_attribute('href')
#         #         item['time'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
#         #         item['react'] = 0
#         #         print(item)
#         #         index += 1
#         #         yield item         
#         #     except Exception as e:
#         #         self.scroll_down_by(driver, self.scroll_distance)
#         #         time.sleep(20)
#         #         driver.implicitly_wait(20)
#         #         continue
#         #     print("index của vòng chính", index)
#         yield SeleniumRequest(
#             url = self.start_urls[2],
#             wait_time = 3,
#             callback = self.parse_personal_page,
#             dont_filter=True,
#         )
#     def parse_personal_page(self, response):
#         item = CrawlFacebookReactItem()
#         indexreact = 1
#         heigh = 600
#         while not self.is_at_bottom(self.driver):
#             if indexreact == 10: break
#             try:
#                 print("index của react select", indexreact)
#                 display_reacts = self.driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62'])[{indexreact}]")    
#                 display_reacts.click()
#                 time.sleep(3)
#                 self.driver.implicitly_wait(3)
#                 dialog = self.driver.find_element(By.XPATH, "//div[@class='xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1iyjqo2 xy5w88m']")
#                 self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dialog)
#                 time.sleep(3)
#                 self.driver.implicitly_wait(3)
#                 react = self.driver.find_elements(By.XPATH, "//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z']")
#                 length = len(react)
#                 if react:
#                     for index in range(2, length + 1):
#                             try:
#                                 print(f"(//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z'])[{index}]/div/div/div/span/div/a")
#                                 # name = driver.find_element(By.XPATH, f"(//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd x1n2onr6 x1ja2u2z x1y1aw1k xwib8y2'])[{index}]/div/div/div/span/div/a").text
#                                 item['idUser']= self.driver.find_element(By.XPATH, f"(//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z'])[{index}]/div/div/div/span/div/a").get_attribute('href')
#                                 print(item)
#                                 yield item
#                             except Exception as e:
#                                 print(f"Lỗi khi lấy tên và URL: {e}")
#                 close_button = self.driver.find_element(By.XPATH, "//div[@class='x1d52u69 xktsk01']")
#                 close_button.click()
#                 indexreact += 1
#             except Exception as e:
#                 print("Lỗi khi hiển thị react")
#                 self.driver.execute_script(f"window.scrollTo(0, {heigh});")
#                 time.sleep(20)
#                 self.driver.implicitly_wait(20)
#                 continue
#             print("index của vòng chính", indexreact)
#         self.driver.quit()
#         return None


import scrapy
from selenium.webdriver.common.by import By
import time
import datetime
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawl_facebook.items import CrawlFacebookItem, CrawlFacebookReactItem
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from shutil import which

class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["www.facebook.com"]
    start_urls = [
        "https://www.facebook.com/",
        "https://www.facebook.com/profile.php?id=61560307553960&sk=friends",
        "https://www.facebook.com/profile.php?id=61560307553960"
    ]
    scroll_distance = 1080

    def scroll_down_by(self, driver, distance):
        driver.execute_script(f"window.scrollBy(0, {distance});")

    def is_at_bottom(self, driver):
        return driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight")

    def __init__(self, *args, **kwargs):
        super(FacebookSpider, self).__init__(*args, **kwargs)
        chrome_path = which("chromedriver")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_service = ChromeService(chrome_path)
        self.driver = Chrome(service=chrome_service, options=chrome_options)
        self.login()

    def login(self):
        self.driver.get(self.start_urls[0])
        time.sleep(3)
        self.driver.implicitly_wait(3)
        input_account = WebDriverWait(self.driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
        )
        input_account.send_keys('boxdat123@gmail.com')
        input_password = self.driver.find_element(By.XPATH, "//input[@id='pass']")
        input_password.send_keys('123456789aA@')
        btn_sign = self.driver.find_element(By.XPATH, "//button[@name='login']")
        btn_sign.click()
    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[1],
            wait_time=3,
            callback=self.parse_friend,
            dont_filter=True
        )

    def parse_friend(self, response):
        self.driver.get(self.start_urls[1])
        time.sleep(3)
        item = CrawlFacebookItem()
        index = 1
        while not self.is_at_bottom(self.driver):
            if index == 2: break
            try:
                print("index của select", index)
                friend = self.driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp'])[{index}]")
                item['name'] = friend.find_element(By.XPATH, ".//div/div/a/span").text
                item['idUser'] = friend.find_element(By.XPATH, ".//div/a").get_attribute('href')
                item['time'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                item['react'] = 0
                print(item)
                index += 1
                yield item         
            except Exception as e:
                self.scroll_down_by(self.driver, self.scroll_distance)
                time.sleep(20)
                self.driver.implicitly_wait(20)
                continue
            print("index của vòng chính", index)
        yield SeleniumRequest(
            url=self.start_urls[2],
            wait_time=3,
            callback=self.parse_personal_page,
            dont_filter=True
        )

    def parse_personal_page(self, response):
        self.driver.get(self.start_urls[2])
        time.sleep(3)
        item = CrawlFacebookReactItem()
        indexreact = 1
        heigh = 600
        while not self.is_at_bottom(self.driver):
            if indexreact == 1: break
            try:
                # print("index của react select", indexreact)
                display_reacts = self.driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62'])[{indexreact}]")
                display_reacts.click()
                time.sleep(3)
                self.driver.implicitly_wait(3)
                dialog = self.driver.find_element(By.XPATH, "//div[@class='xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1iyjqo2 xy5w88m']")
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dialog)
                time.sleep(3)
                self.driver.implicitly_wait(3)
                react = self.driver.find_elements(By.XPATH, "//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z']")
                length = len(react)
                if react:
                    for index in range(2, length + 1):
                        try:
                            print(f"(//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z'])[{index}]/div/div/div/span/div/a")
                            item['idUser'] = self.driver.find_element(By.XPATH, f"(//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd xz9dl7a xsag5q8 x1n2onr6 x1ja2u2z'])[{index}]/div/div/div/span/div/a").get_attribute('href')
                            print(item)
                            yield item
                        except Exception as e:
                            print(f"Lỗi khi lấy tên và URL: {e}")
                close_button = self.driver.find_element(By.XPATH, "//div[@class='x1d52u69 xktsk01']")
                close_button.click()
                indexreact += 1
            except Exception as e:
                print("Lỗi khi hiển thị react")
                self.driver.execute_script(f"window.scrollTo(0, {heigh});")
                time.sleep(20)
                self.driver.implicitly_wait(20)
                continue
            print("index của vòng chính", indexreact)
        self.driver.quit()
        return None
