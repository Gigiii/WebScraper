import scrapy
from scrapy.crawler import CrawlerProcess

class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["www.bbc.com"]
    start_urls = ["https://www.bbc.com"]

    def parse(self, response):
        print("[MY RESPONSE]")
        titles = response.css('a.media__link::text').extract()
        print(titles)


# Create a CrawlerProcess instance
process = CrawlerProcess()

# Add your spider to the process
process.crawl(BbcSpider)

# Start the crawling process
process.start()