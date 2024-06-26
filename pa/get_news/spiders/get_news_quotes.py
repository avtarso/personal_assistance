import scrapy

from get_news.items import QuoteItem


class GetNewsQuotesSpider(scrapy.Spider):
    name = "get_news_quotes"

    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):

        for quote in response.xpath("/html//div[@class='quote']"):

            item = QuoteItem()

            item["tags"] = quote.xpath("div[@class='tags']/a/text()").extract()
            item["author"] = quote.xpath("span/small/text()").get()
            item["quote"] = quote.xpath("span[@class='text']/text()").get()

            yield item

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)