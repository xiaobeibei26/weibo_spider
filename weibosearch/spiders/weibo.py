# -*- coding: utf-8 -*-
import scrapy,re
import tushare as ts
from scrapy import FormRequest,Request
from weibosearch.items import WeibosearchItem
class WeiboSpider(scrapy.Spider):
    name = "weibo"
    allowed_domains = ["weibo.cn"]
    start_urls = ['http://weibo.cn/']
    search_url = 'https://weibo.cn/search/mblog'
    max_page = 100

    def start_requests(self):
        result=ts.get_zz500s()
        kewwords=result['code'].tolist()
        for keyword in kewwords:
            # keyword ='勒布朗詹姆斯'
            url = '{url}?&keyword={keyword}'.format(url=self.search_url,keyword=keyword)
            for page in range(1,100):
                date={
                    'mp':str(self.max_page),
                    'page':str(page)
                }
                yield FormRequest(url,callback=self.parse_index,formdata=date,meta={'keyword':keyword})

    def parse_index(self, response):
        weibos=response.xpath('//div[@class="c" and contains(@id,"M_")]')
        for weibo in weibos:
            is_forward = weibo.xpath('.//span[@class="cmt"]').extract_first(None)

            if is_forward:
                detail_url = weibo.xpath('.//a[contains(.,"原文评论[")]//@href').extract_first()
            else:
                detail_url=weibo.xpath('.//a[contains(.,"评论[")]//@href').extract_first()
            yield Request(url=detail_url,callback=self.parse_detail,meta={'keyword':response.meta['keyword']})
    def parse_detail(self,response):
        weibo_item =WeibosearchItem()
        id = re.search('comment\/(.*?)\?',response.url).group(1)
        url = response.url
        content=''.join(response.xpath('//div[@id="M_"]//span[@class="ctt"]//text()').extract()).strip().replace('\u200b','')
        comment_count = response.xpath('//span[@class="pms"]//text()').re_first('评论\[(.*?)\]')
        forward_count = response.xpath('//a[contains(.,"转发[")]//text()').re_first('转发\[(.*?)\]')
        like_count=response.xpath('//a[contains(.,"赞[")]//text()').re_first('赞\[(.*?)\]')
        publish_time=response.xpath('//div[@id="M_"]//span[@class="ct"]//text()').extract_first(default=None)
        user = response.xpath('//*[@id="M_"]/div[1]/a[1]/text()').extract_first()
        keyword=response.meta['keyword']
        for field in weibo_item.fields:
            try:
                weibo_item[field]=eval(field)
            except:
                self.logger.debug('Field is not define')

        yield weibo_item

        # print(content,publish_time,user,comment_count,forward_count,like_count)























