import scrapy
from selenium.webdriver.common.by import By
import time
import datetime
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawl_facebook.items import CrawlFacebookItem, CrawlFacebookReactItem, CrawlFacebookCommentItem
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
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-logging")
        chrome_options.add_argument('--log-level=3')
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
        input_account.send_keys('')
        input_password = self.driver.find_element(By.XPATH, "//input[@id='pass']")
        input_password.send_keys('')
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
            # if index == 10: break
            try:
                print("index của select", index)
                friend = self.driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp'])[{index}]")
                item['name'] = friend.find_element(By.XPATH, ".//div/div/a/span").text
                item['idUser'] = friend.find_element(By.XPATH, ".//div/a").get_attribute('href')
                item['time'] = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                item['react'] = 0
                item['comment'] = 0
                print(item)
                index += 1
                yield item         
            except Exception as e:
                self.scroll_down_by(self.driver, self.scroll_distance)
                time.sleep(3)
                self.driver.implicitly_wait(3)
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
        item1 = CrawlFacebookCommentItem()
        indexreact = 1
        indexcomment = 1
        heigh = 1080
        while not self.is_at_bottom(self.driver):
                # if indexreact == 11: break
                    try:
                        display_reacts = self.driver.find_element(By.XPATH, f"(//div[@class='x6s0dn4 x78zum5 x1iyjqo2 x6ikm8r x10wlt62'])[{indexreact}]")
                        display_reacts.click()
                        time.sleep(3)
                        self.driver.implicitly_wait(3)
                        dialog = self.driver.find_element(By.XPATH, "//div[@class='xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1e4zzel x1tbbn4q x1y1aw1k x4uap5 xwib8y2 xkhd6sd']")
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dialog)
                        time.sleep(3)
                        self.driver.implicitly_wait(3)
                        reacts = self.driver.find_elements(By.XPATH, "//div[@class='xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1e4zzel x1tbbn4q x1y1aw1k x4uap5 xwib8y2 xkhd6sd']/div/div")
                        for react in reacts:
                            break
                            try:
                                item['idUser'] = react.find_element(By.XPATH, ".//div/div/div/div/div/div/div/span/div/a").get_attribute('href')
                                print("react ")
                                print(item)
                                yield item
                            except Exception as e:
                                print(f"Lỗi khi lấy tên và URL: {e}")
                                continue
                        close_button = self.driver.find_element(By.XPATH, "//div[@class='x1d52u69 xktsk01']")
                        close_button.click()
                        indexreact += 1
                    except Exception as e:
                        print("Lỗi khi hiển thị react")
                    try:
                        display_comments = self.driver.find_element(By.XPATH, f"(//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj'])[{indexcomment}]")
                        display_comments.click()
                        time.sleep(3)
                        self.driver.implicitly_wait(3)
                        dialog = self.driver.find_element(By.XPATH, "//div[@class='xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1iyjqo2 xy5w88m']")
                        self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", dialog)
                        time.sleep(3)
                        self.driver.implicitly_wait(3)
                        comments= self.driver.find_elements(By.XPATH, "//div[@class='x1gslohp']/div")
                        if comments:
                            for comment in comments:
                                break
                                try:
                                    url = comment.find_element(By.XPATH, ".//div/div/div/div/div/span/a").get_attribute('href')
                                    print("comment")
                                    print(url)
                                    item1['idUser'] = url
                                    yield item1
                                except Exception as e:
                                    print(f"Lỗi khi lấy tên và URL: {e}")
                                    continue
                        close_button = self.driver.find_element(By.XPATH, "//div[@class='x1d52u69 xktsk01']")
                        close_button.click()
                        indexcomment += 1
                    except Exception as e:
                        print("Lỗi khi hiển thị comment")
                    self.driver.execute_script(f"window.scrollTo(0, {heigh});")
                    time.sleep(3)
                    self.driver.implicitly_wait(3)
                    print("index của vòng chính react ", indexreact)
                    print("index của vòng chính comment ", indexcomment)
                    indexreact = indexcomment = max(indexreact, indexcomment)
        self.driver.quit()
        return None
