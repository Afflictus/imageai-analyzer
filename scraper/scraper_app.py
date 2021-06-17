import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def scrap(start_urls):
    start_urls = start_urls

    process = CrawlerProcess(get_project_settings())
    process.crawl("test", start_urls=start_urls)
    try:
        process.start()
    except Exception as e:
        print("Во время запуска скрапера произошла ошибка, проверьте список сайтов для скрапинга. Подробности: ", e)
