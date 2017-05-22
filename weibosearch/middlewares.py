# -*- coding:utf-8 -*-
import random,logging

from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from weibosearch.useragent import agents
from scrapy.exceptions import IgnoreRequest
import redis,random,logging,json
class UserAgentmiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

class CookiesMddleware():
    def __init__(self,url,port):
        self.loggger = logging.getLogger(__name__)
        self._db = redis.Redis(host=url, port=port)
    def get_cookie(self):
        try:
            key= random.choice(self._db.keys('cookies:*'))
            return json.loads(self._db.get(key).decode())
        except Exception as e:
            print(e,'获取cookie失败')
    def get_ip(self):
        proxies = self._db.lrange('proxies', 0, -1)
        return random.choice(proxies).decode()
    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            url=crawler.settings.get('REDIS_URL'),
            port=crawler.settings.get('REDIS_PORT'),
        )
    def process_request(self,request,spider):
        cookies =self.get_cookie()
        # proxies=self.get_ip()
        if cookies:
            request.cookies = cookies
            # request.meta['proxy'] ='http://{}'.format(proxies)
            self.loggger.debug('Using Cookies'+json.dumps(cookies))
        else:
            self.loggger.debug('No Valid Cookies')



    def process_response(self,request,response,spider):
        if response.status in  [301,302,303,300]:#有些cookie失效了，会被重定向
            try:
                redirect_url = response.headers['location']
                if 'passport' in redirect_url:
                    self.loggger.warning('Need login,New Cookies')
                elif 'weibo.cn/security' in redirect_url:
                    self.loggger.warning('Account is locked!')
                request.cookies =self.get_cookie()
                return request
            except:
                raise IgnoreRequest
        elif response.status in [414]:#链接太长
            return request
        else:
            return response