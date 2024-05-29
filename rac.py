  # # lấy comment
                # try:
                #     try:
                #         indexcomment += 1
                #         display_comment = driver.find_element(By.XPATH, f"(//div[@class='x9f619 x1n2onr6 x1ja2u2z x78zum5 x2lah0s x1qughib x1qjc9v5 xozqiw3 x1q0g3np xykv574 xbmpl8g x4cne27 xifccgj'])[{indexcomment}]")
                #     except:
                #         indexcomment -= 1
                #     display_comment.click()
                #     time.sleep(3)
                #     driver.implicitly_wait(3)
                #     for i in range(10):
                #           driver.execute_script(f"window.scrollTo(0, 1080);")
                #     driver.implicitly_wait(3)
                #     time.sleep(3)
                #     comments = driver.find_elements(By.XPATH, "//div[@class='x169t7cy x19f6ikt']")
                #     for comment in comments:
                #         url = driver.find_element(By.XPATH, "../div/div/div/div/div/div/span/a").get_attribute('href')
                #         name =  driver.find_element(By.XPATH, "../div/div/div/div/div/div/span/a/span/span").text
                #         yield {"name": name, "url": url}
                #     close_button = driver.find_element(By.XPATH, "//div[@aria-label='Đóng']")
                #     close_button.click()
                # except Exception as e:
                #     print(f"Lỗi khi lấy comment")
                # //body







                #file lúc chưa chỉnh sửa middle ware
# import scrapy
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from shutil import which
# from selenium.webdriver.chrome.service import Service
# from scrapy.selector import Selector
# import time
# from scrapy_selenium import SeleniumRequest
# from selenium.webdriver.support.ui import WebDriverWait
# from crawl_facebook.items import CrawlFacebookItem
# class FacebookSpider(scrapy.Spider):
#     name = "facebook"
#     allowed_domains = ["www.facebook.com"]
#     start_urls = ["https://www.facebook.com/","https://www.facebook.com/maybetuandat/friends" ,"https://www.facebook.com/maybetuandat"]
#     scroll_distance = 600
#     def start_requests(self):
#         yield SeleniumRequest(
#             url = self.start_urls[0],
#             wait_time = 3,
#             callback = self.init_requests
#         )
#     def init_requests(self, response):
#         yield SeleniumRequest(
#             url = self.start_urls[1],
#             wait_time = 3,
#             callback = self.parse_friend,
#                dont_filter=True  
#         )
#     def scroll_down_by(self,driver, distance):
#         driver.execute_script(f"window.scrollBy(0, {distance});")
#     def is_at_bottom(self,driver):
#         return driver.execute_script("return window.innerHeight + window.scrollY >= document.body.scrollHeight")
#     def parse_friend(self, response):
#         item = CrawlFacebookItem()
#         driver = response.meta['driver']
#         # for i in range(5):
#         #     self.scroll_down_by(driver, self.scroll_distance)
#         #     time.sleep(3)
#         #     if self.is_at_bottom(driver):
#         #         break
#         driver.implicitly_wait(10)
#         try:
#             friends = driver.find_elements(By.XPATH, "//div[@class='x6s0dn4 x1lq5wgf xgqcy7u x30kzoy x9jhf4c x1olyfxc x9f619 x78zum5 x1e56ztr xyamay9 x1pi30zi x1l90r2v x1swvt13 x1gefphp']")
        
#         # Kiểm tra xem danh sách bạn bè có rỗng không
#             if friends:
#                 for friend in friends:
#                 # Kiểm tra xem friend có trong danh sách không
#                     if friend in friends:
#                         item['name'] = friend.find_element(By.XPATH, ".//div/div/a/span").text
#                         item['url'] = friend.find_element(By.XPATH, ".//div/a").get_attribute('href')
#                         yield item
#         except Exception as e:
#             print(e)
#             print("in ra loi chu khong phai bi loi")
#         yield SeleniumRequest(
#             url = self.start_urls[2],
#             wait_time = 3,
#             callback = self.parse_personal_page,
#             dont_filter=True
#         )
#     def parse_personal_page(self, response):
#         driver = response.meta['driver']
#         driver.implicitly_wait(10)


