import scrapy
import json
from codecs import encode
from scrapy.http import Request
from shanbaySpider.shanbayitems import ShanbayItem


class shanbaySpider(scrapy.Spider):
    name = 'shanbay'
    allow_domains = ["www.shanbay.com"]

    def start_requests(self):
        for i in range(1, 5):
            url = "https://www.shanbay.com/api/v1/forum/11077/thread/?page={}".format(i)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        res = json.loads(response.body)
        threads = res['data']['threads']
        threadItems = []
        for dict in threads:
            threadItem = ShanbayItem()
            threadItem['title'] = dict['title']
            threadItem['author'] = dict['author']['nickname']
            threadItem['topic_post_time'] = dict['topic_post_time']
            threadItems.append(threadItem)
        return threadItems
