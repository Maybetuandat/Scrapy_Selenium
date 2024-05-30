# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# # useful for handling different item types with a single interface






import pymongo
import datetime
import re
from scrapy.exceptions import DropItem
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver import Edge
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from shutil import which
import time
from crawl_facebook.items import CrawlFacebookItem, CrawlFacebookReactItem
#pipeline của thằng lấy danh sách bạn bè 
class CrawlFacebookPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
            
        )
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
    def process_item(self, item, spider):
        edge_path = which("msedgedriver")
        edge_options = EdgeOptions()
        edge_options.add_argument("--incognito")
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu") 
        edge_options.add_argument("--log-level=3")
        edge_options.add_argument("--no-sandbox")
        edge_options.add_argument("--disable-dev-shm-usage")
        edge_options.add_argument("--disable-extensions")
        edge_options.add_argument("--disable-logging")
        edge_service = EdgeService(edge_path)
        driver_edge = Edge(service=edge_service, options=edge_options)
        driver_edge.get(item.get('idUser'))
        time.sleep(10)
        driver_edge.implicitly_wait(10)
        html = driver_edge.page_source
        match = re.search(r'"userID":"(\d+)"', html)
        if match:
            user_id = match.group(1)
        else:
            user_id = None
        if user_id:
            item['idUser'] = user_id
        driver_edge.quit()
        if 'time' in item:
            try:
                item['time'] = datetime.datetime.strptime(item['time'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise DropItem(f"Failed to parse 'time' field: {e}")
        if isinstance(item, CrawlFacebookItem):  
            try:
                existing_item = self.db[self.mongo_collection].find_one({'idUser': item.get('idUser')})
                if existing_item:
                    updates = {}
                    if existing_item.get('name') != item.get('name'):
                        updates['name'] = item.get('name')
                    if existing_item.get('react') and existing_item.get('react') != 0:
                        updates['react'] = 0
                    if updates:
                        self.db[self.mongo_collection].update_one(
                            {'_id': existing_item['_id']},
                            {'$set': updates}
                        )
                else:
                    self.db[self.mongo_collection].insert_one(dict(item))   
                    return item
            except:
                raise DropItem(f"Failed to update item in MongoDB: {e}")
        elif isinstance(item, CrawlFacebookReactItem):
          #drop database 
            existing_item = self.db[self.mongo_collection].find_one({'idUser': item.get('idUser')})
            if existing_item:
               self.db[self.mongo_collection].update_one(
                    {'_id': existing_item['_id']},
                    {'$inc': {'react': 1}}
                )
            else:
                raise DropItem(f"Missing one of the fields in {item}")
        else:
            raise DropItem(f"Unknown item type: {type(item)}")
    def close_spider(self, spider):
        self.client.close()


