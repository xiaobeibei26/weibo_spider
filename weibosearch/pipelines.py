
import re,time,pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from weibosearch.items import  WeibosearchItem

class WeibosearchPipeline(object):
    def parse_time(self,datetime):
        if re.match('\d+月\d+日',datetime):
            datetime=time.strftime('%Y-',time.localtime()) + datetime
        if re.match('\d+分钟前',datetime):
            minute = re.match('(\d+)',datetime).group(1)
            datetime=time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()-float(minute)))
        if re.match('今天.*',datetime):
            datetime=re.match('今天(.*)',datetime).group().strip()
            datetime=time.strftime('%Y-%m-%d',time.localtime())+' '+datetime
        return datetime
    def process_item(self, item, spider):

        if isinstance(item,WeibosearchItem):
            if item.get('content'):
                item['content']=item['content'].lstrip(':').strip()
                if item.get('publish_time'):
                    item['publish_time'] = item['publish_time'].strip()
                    item['publish_time']=self.parse_time(item['publish_time'])
        return item

class MonoPipeline():
    def __init__(self,mongo_url,mongo_db):
        self.mongo_url= mongo_url
        self.mongo_db = mongo_db
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mongo_url=crawler.settings.get('MONGO_URL'),
            mongo_db =crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(self.mongo_url)
        self.db=self.client[self.mongo_db]
    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):#每一条微博有自己唯一的id，以此来去重或者更新
        self.db[item.table_name].update({'id':item.get('id')},{'$set':dict(item)},True)
        print('一条数据插入成功')



