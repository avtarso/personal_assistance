import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

from scrapy.utils.project import get_project_settings


def func(q, spider, uid):

    class CustomSpider(spider):
        request_user_id = uid

    try:
        runner = crawler.CrawlerRunner(get_project_settings())
        deferred = runner.crawl(CustomSpider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


# The wrapper to make spider run more times
def run_get_news_spider(spider, uid):
    q = Queue()
    p = Process(target=func, args=(q, spider, uid))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result
