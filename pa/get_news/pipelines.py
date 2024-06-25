# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from news.models import NewsQuote, NewsEconomics, NewsPolitics
from django.core.exceptions import ObjectDoesNotExist


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
                time=adapter["time"], text=adapter["text"], url=adapter["url"]
            )
        elif spider.name == "get_news_politics":
            data = NewsPolitics.objects.create(
                time=adapter["time"], text=adapter["text"], url=adapter["url"]
            )
        else:
            tags = ", ".join(adapter["tags"])
            data = NewsQuote.objects.create(
                quote=adapter["quote"], author=adapter["author"], tags=tags
            )
        data.save()

        return item
