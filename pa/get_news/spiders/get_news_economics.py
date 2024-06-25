import scrapy

from get_news.items import EconomicsItem


class GetNewsEconomicsSpider(scrapy.Spider):
    name = "get_news_economics"
    allowed_domains = ["ukr.net"]
    start_urls = ["https://www.ukr.net/news/economics.html"]

    def parse(self, response):

        for news in response.xpath("/html//article//section[@class='im']"):
            item = EconomicsItem()

            item["time"] = news.xpath("time/text()").get()
            item["text"] = news.xpath("div/div/a/text()").get()
            item["url"] = news.xpath("div/div/a/@href").get()

            yield item
