# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from news.models import NewsQuote, NewsEconomics, NewsPolitics, NewsWeather


class StripPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        for key, value in adapter.items():
            if key == "tags":
                for i in range(len(value)):
                    value[i] = value[i].strip()
            else:
                adapter[key] = value.strip()

        return item


class DatabasePipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        if spider.name == "get_news_economics":
            data = NewsEconomics.objects.create(
                time=adapter["time"],
                text=adapter["text"],
                url=adapter["url"],
                added_by_id=spider.request_user_id,
            )
        elif spider.name == "get_news_politics":
            data = NewsPolitics.objects.create(
                time=adapter["time"],
                text=adapter["text"],
                url=adapter["url"],
                added_by_id=spider.request_user_id,
            )
        elif spider.name == "get_news_weather":
            data = NewsWeather.objects.create(
                day=adapter["day"],
                month=adapter["month"],
                degree=adapter["degree"],
                added_by_id=spider.request_user_id,
            )
        else:
            tags = ", ".join(adapter["tags"])
            data = NewsQuote.objects.create(
                quote=adapter["quote"],
                author=adapter["author"],
                tags=tags,
                added_by_id=spider.request_user_id,
            )

        data.save()

        return item
