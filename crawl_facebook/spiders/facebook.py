import scrapy
from selenium.webdriver.common.by import By
import time
import re
import datetime
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from crawl_facebook.items import CrawlFacebookItem, CrawlFacebookReactItem
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from shutil import which
class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["www.facebook.com"]
    start_urls = ["https://www.facebook.com/","https://www.facebook.com/profile.php?id=61560307553960&sk=friends" ,"https://www.facebook.com/profile.php?id=61560307553960"]
    scroll_distance = 1080
    
    def __init__(self, *args, **kwargs):
        super(FacebookSpider, self).__init__(*args, **kwargs)
        chrome_path = which("chromedriver")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--incognito")
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu") 
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        chrome_service = ChromeService(chrome_path)
        self.driver = Chrome(service=chrome_service, options=chrome_options)
        
    def start_requests(self):
        yield SeleniumRequest(
            url = self.start_urls[0],
            wait_time = 3,
            callback = self.init_requests,
            meta={'driver': self.driver}
        )
    def init_requests(self, response):
        yield SeleniumRequest(
            url = self.start_urls[1],
            wait_time = 3,
            callback = self.parse_friend,
               dont_filter=True  ,
               meta={'driver': self.driver}
        )
    def scroll_down_by(self,driver, distance):
        driver.execute_script(f"window.scrollBy(0, {distance});")
    def is_at_bottom(self,driver):
        return driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight")
    def parse_friend(self, response):
        item = CrawlFacebookItem()
        driver = response.meta['driver']
        index = 1
        while not self.is_at_bottom(driver):
            if index == 50: break
            try:
                print("index của select", index)
                friend = driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp'])[{index}]")
                item['name'] = friend.find_element(By.XPATH, ".//div/div/a/span").text
                item['idUser'] = friend.find_element(By.XPATH, ".//div/a").get_attribute('href')
                item['time'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                item['react'] = 0
                print(item)
                index += 1
                yield item         
            except Exception as e:
                self.scroll_down_by(driver, self.scroll_distance)
                time.sleep(20)
                driver.implicitly_wait(20)
                continue
            print("index của vòng chính", index)
        yield SeleniumRequest(
            url = self.start_urls[2],
            wait_time = 3,
            callback = self.parse_personal_page,
            dont_filter=True,
            meta={'driver': self.driver}
        )
    def parse_personal_page(self, response):
        driver = response.meta['driver']
        item = CrawlFacebookReactItem()
        indexreact = 1
        heigh = 300
        while not self.is_at_bottom(driver):
            if indexreact == 5: break
            try:
                print("index của react select", indexreact)
                display_reacts = driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62'])[{indexreact}]")    
                display_reacts.click()
                time.sleep(5)
                driver.implicitly_wait(5)
                react = driver.find_elements(By.XPATH, "//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd x1n2onr6 x1ja2u2z x1y1aw1k xwib8y2']")
                length = len(react)
                if react:
                    for index in range(2, length + 1):
                            try:
                                # name = driver.find_element(By.XPATH, f"(//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd x1n2onr6 x1ja2u2z x1y1aw1k xwib8y2'])[{index}]/div/div/div/span/div/a").text
                                item['idUser']= driver.find_element(By.XPATH, f"(//div[@class='x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli x4uap5 xkhd6sd x1n2onr6 x1ja2u2z x1y1aw1k xwib8y2'])[{index}]/div/div/div/span/div/a").get_attribute('href')
                                print(item)
                                yield item
                            except Exception as e:
                                print(f"Lỗi khi lấy tên và URL: {e}")
                close_button = driver.find_element(By.XPATH, "//div[@class='x1d52u69 xktsk01']")
                close_button.click()
                indexreact += 1
            except Exception as e:
                print("Lỗi khi hiển thị react")
                driver.execute_script(f"window.scrollTo(0, {heigh});")
                time.sleep(15)
                driver.implicitly_wait(15)
                continue
            print("index của vòng chính", indexreact)
        driver.quit()
        return None
