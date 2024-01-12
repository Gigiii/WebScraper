import scrapy
from scrapy.exporters import JsonItemExporter
from news_scraper.items import NewsScraperItem

class UkNewsSpider(scrapy.Spider):
    name = "uk_news"
    url_parsing_pairs = {
                         "https://www.bbc.com/news": "h3.gs-c-promo-heading__title::text",
                        #  "https://www.theguardian.com/europe": "span.dcr-1ay6c8s::text",
                        #  "https://www.telegraph.co.uk/news/": "span.list-headline__text>span::text",
                        #  "https://www.mirror.co.uk/news/": "div.story__title>h2::text",
                        #  "https://www.express.co.uk/news": "span.rh-header::text, h4::text"
                        }
    start_urls = list(url_parsing_pairs.keys())
    
    def parse(self, response):
        print(f"[RESPONSE URL] : {response.url}")
        titles = response.css(UkNewsSpider.url_parsing_pairs[response.url]).extract()
        item = NewsScraperItem()
        item['titles'] = titles
        yield item


class AmericanNewsSpider(scrapy.Spider):
    name = "american_news"
    url_parsing_pairs = {
                         "https://www.washingtonpost.com/": "h2.wpds-c-iiQaMf>a>span::text"}
    start_urls = list(url_parsing_pairs.keys())

    def parse(self, response):
        print(f"[RESPONSE URL] : {response.url}")
        titles = response.css(AmericanNewsSpider.url_parsing_pairs[response.url]).extract()
        item = NewsScraperItem()
        item['titles'] = titles
        yield item
