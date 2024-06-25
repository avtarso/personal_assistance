import scrapy

from get_news.items import PoliticsItem


class GetNewsPoliticsSpider(scrapy.Spider):
    name = "get_news_politics"
    allowed_domains = ["ukr.net"]
    start_urls = ["https://www.ukr.net/news/politics.html"]

    def parse(self, response):

        for news in response.xpath("/html//article//section[@class='im']"):
            item = PoliticsItem()

            item["time"] = news.xpath("time/text()").get()
            item["text"] = news.xpath("div/div/a/text()").get()
            item["url"] = news.xpath("div/div/a/@href").get()

            yield item
