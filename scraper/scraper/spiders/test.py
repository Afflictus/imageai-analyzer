import scrapy

class ScrapTest(scrapy.Spider):
    name = "test"

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_images)

    def parse_images(self, response, **kwargs):
        url = response.request.url
        img_urls = response.css('img::attr(src)').getall()
        img_urls = [response.urljoin(i) for i in img_urls]
        yield {
            "url": url,
            "images": img_urls,
        }

    def parse(self, response, **kwargs):
        url = response.request.url
        status_code = response.status
        user_agent = response.request.headers['user-agent']
        title = response.css("title::text").get()
        yield {
            "url": url,
            "status_code": status_code,
            "user_agent": user_agent,
            "title": title,
        }
