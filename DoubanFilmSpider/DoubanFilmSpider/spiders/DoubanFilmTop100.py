import scrapy
import json
from scrapy.http import Request
from DoubanFilmSpider.doubanfilmitems import DoubanfilmspiderItem


class DoubanFilmSpider(scrapy.Spider):
    name = "DoubanFilmTop100"
    allow_domains = ["movie.douban.com"]

    def start_requests(self):
        for i in range(0, 5):
            url = "https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=%E7%94%B5%E5%BD%B1&start={}".format(i*20)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        res = json.loads(response.body)
        filmlists = res['data']
        filmItems = []
        for dict in filmlists:
            filmItem = DoubanfilmspiderItem()
            filmItem['title'] = dict['title']
            filmItem['coverpic'] = dict['cover']
            filmItem['url'] = dict['url']
            filmItem['rate'] = dict['rate']
            filmItem['directors'] = dict['directors']
            filmItem['casts'] = dict['casts']
            filmItems.append(filmItem)
        return filmItems
