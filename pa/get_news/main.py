import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

from scrapy.utils.project import get_project_settings

from .spiders.get_news_quotes import GetNewsQuotesSpider
from .spiders.get_news_economics import GetNewsEconomicsSpider
from .spiders.get_news_politics import GetNewsPoliticsSpider


def func(q, spider):
    try:
        runner = crawler.CrawlerRunner(get_project_settings())
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def common(spider):
    q = Queue()
    p = Process(target=func, args=(q, spider))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


# The wrapper to make spider run more times
def run_get_news_quotes_spider(spider=GetNewsQuotesSpider):
    common(spider=GetNewsQuotesSpider)


def run_get_news_economics_spider(spider=GetNewsEconomicsSpider):
    common(spider=GetNewsEconomicsSpider)


def run_get_news_politics_spider(spider=GetNewsPoliticsSpider):
    common(spider=GetNewsPoliticsSpider)
