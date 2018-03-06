import scrapy
from WangyiNewsSpider.WangyiNewsItems import WangyinewsItem


class WangyiNewsSpider(scrapy.Spider):
    name = "newslist"
    # allow_domains = ["news.163.com"]
    start_urls = ["http://news.163.com/rank/"]

    def parse(self, response):
        for url in response.css('.more a::attr(href)').extract():
            yield scrapy.Request(url, callback=self.parse_news)

    def parse_news(self, response):    
        for new_url in response.xpath('//tr/td/a/@href').extract():
            yield scrapy.Request(new_url,callback=self.parse_news_detail)

    def parse_news_detail(self,response):
        yield{
            'new_item' :response.xpath('//div/h1/text()').extract(),
            'new_url' :response.url,
        }
        
        
