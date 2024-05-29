# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html



# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from shutil import which
import time
from selenium.webdriver.chrome.options import Options
class CrawlFacebookSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
class SeleniumMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=scrapy.signals.spider_closed)   # ham mac dinh trong spider 
        return s

    def process_request(self, request, spider):
        url = request.url
        driver = request.meta.get('driver')
        driver.get(request.url)                    
        if request.url == "https://www.facebook.com/":
            self.login(driver)
        else:
            time.sleep(5)  
        request.meta['driver'] = driver # gửi lại driver cho spider
        

    def login(self, driver):
        input_account = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
        )
        input_account.send_keys('')

        input_password = driver.find_element(By.XPATH, "//input[@id='pass']")
        input_password.send_keys('')

        btn_sign = driver.find_element(By.XPATH, "//button[@name='login']")
        btn_sign.click()
    def spider_closed(self, spider):
        driver = spider.driver
        driver.quit()