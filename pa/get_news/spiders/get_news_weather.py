import scrapy

from get_news.items import WeatherItem


class GetNewsWeatherSpider(scrapy.Spider):
    name = "get_news_weather"
    allowed_domains = ["meteo.ua"]
    start_urls = ["https://meteo.ua/ua/34/kiev/month"]

    def parse(self, response):

        for news in response.xpath("/html//div[@class='menu-basic__item']"):
            item = WeatherItem()

            item["day"] = news.xpath("a/div[@class='menu-basic__day']/text()").get()
            item["month"] = news.xpath("a/div[@class='menu-basic__month']/text()").get()
            item["degree"] = news.xpath(
                "a/div[@class='menu-basic__degree']/text()"
            ).get()

            yield item
