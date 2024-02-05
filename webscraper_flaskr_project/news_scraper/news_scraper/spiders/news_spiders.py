import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
import scrapy

class NewsScraperItem(scrapy.Item):
    """
    Item Class for sending our items through the filter pipeline.
    """
    titles = scrapy.Field()

class AmericanNewsSpider(scrapy.Spider):
    """
    Spider for scraping American news headlines from various websites.
    """
    name = "American_news"
    url_parsing_pairs = {
        "https://www.washingtonpost.com/": "h2>a>span::text",
        "https://www.nydailynews.com/news/politics/": "h2>a>span::text",
        "https://eu.usatoday.com/news/nation/": "div.p1-title-spacer::text, div.display-6::text, div.display-4::text",
        "https://www.chicagotribune.com/news/breaking/": "h2::text",
        "https://www.latimes.com/": "h1>a::text"
    }
    start_urls = list(url_parsing_pairs.keys())

    def parse(self, response):
        """
        Extracts titles from URLs, creates a title item, and sends it to the pipeline.
        Args:
            response (scrapy.http.Response): The response object containing the scraped data.
        """
        titles = response.css(AmericanNewsSpider.url_parsing_pairs[response.url]).extract()
        item = NewsScraperItem()
        item['titles'] = titles
        yield item

class UkNewsSpider(scrapy.Spider):
    """
    Spider for scraping UK news headlines from various websites.
    """
    name = "Britain_news"
    url_parsing_pairs = {
        "https://www.bbc.com/news": "h3::text",
        "https://www.theguardian.com/europe": "h3>span::text",
        "https://www.telegraph.co.uk/news/": "h2>a>span>span::text",
        "https://www.mirror.co.uk/news/": "h2::text",
        "https://www.express.co.uk/news": "span.rh-header::text, h4::text"
    }
    start_urls = list(url_parsing_pairs.keys())

    def parse(self, response):
        """
        Extracts titles from URLs, creates a title item, and sends it to the pipeline.
        Args:
            response (scrapy.http.Response): The response object containing the scraped data.
        """
        titles = response.css(UkNewsSpider.url_parsing_pairs[response.url]).extract()
        item = NewsScraperItem()
        item['titles'] = titles
        yield item

class GermanNewsSpider(scrapy.Spider):
    """
    Spider for scraping German news headlines from various websites.
    """
    name = "Germany_news"
    url_parsing_pairs = {
        "https://www.dw.com/en/top-stories/s-9097": "h3>a>span::text, h4>a>span::text",
        "https://www.spiegel.de/international/germany/": "span.align-middle::text",
        "https://www.zeit.de/english/index": "h3>span.zon-teaser-standard__title::text",
        "https://www.welt.de/english-news/": "h4>a::text",
        "https://www.deutschland.de/en/news": "div.article-teaser-big__headline::text, div.teaser-small__headline::text"
    }
    start_urls = list(url_parsing_pairs.keys())

    def parse(self, response):
        """
        Extracts titles from URLs, creates a title item, and sends it to the pipeline.
        Args:
            response (scrapy.http.Response): The response object containing the scraped data.
        """
        titles = response.css(GermanNewsSpider.url_parsing_pairs[response.url]).extract()
        item = NewsScraperItem()
        item['titles'] = titles
        yield item


class SingaporeNewsSpider(scrapy.Spider):
    """
    Spider for scraping Singapore news headlines from various websites.
    """
    name = "Singapore_news"
    url_parsing_pairs = {
        "https://www.straitstimes.com/global": "h5>a::text",
        "https://www.todayonline.com/singapore": "h4>a::text, h3>a::text",
        "https://www.businesstimes.com.sg/": "a.text-gray-850::text",
        "https://weekender.com.sg/": "h4>a::text",
        "https://mothership.sg/": "h1::text"
    }
    start_urls = list(url_parsing_pairs.keys())

    def parse(self, response):
        """
        Extracts titles from URLs, creates a title item, and sends it to the pipeline.
        Args:
            response (scrapy.http.Response): The response object containing the scraped data.
        """
        titles = response.css(SingaporeNewsSpider.url_parsing_pairs[response.url]).extract()
        item = NewsScraperItem()
        item['titles'] = titles
        yield item
