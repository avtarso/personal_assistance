import scrapy

from get_news.items import WeatherByCityItem


class GetNewsWeatherByCitySpider(scrapy.Spider):
    name = "get_news_weather_by_city"
    allowed_domains = ["meteo.ua"]
    start_urls = ["https://meteo.ua/ua"]

    def parse(self, response):

        for news in response.xpath("/html//div[@class='info-tiles__col']"):
            item = WeatherByCityItem()

            item["url"] = (
                self.start_urls[0].removesuffix("/ua")
                + news.xpath("a[@class='info-tile']/@href").get()
            )

            item["city"] = news.xpath("a/div[@class='info-tile__city']/text()").get()

            item["degree"] = news.xpath(
                "a/div[@class='info-tile__degree']/text()"
            ).get()

            item["cloudy"] = news.xpath("a/div[@class='info-tile__label']/text()").get()

            item["humidity"] = news.xpath(
                "a/div[@class='info-tile__value']/text()"
            ).get()

            yield item
