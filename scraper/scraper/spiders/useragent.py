import scrapy


class UserAgent(scrapy.Spider):
    name = "checkua"
    start_urls = [
        'google.com'
    ]

    def parse(self, response, **kwargs):
        url = response.request.url
        ua = response.css("div.detected_result div.value a::text").get()
        yield {
            "url": url,
            "user_agent": ua
        }
