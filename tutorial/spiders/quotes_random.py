# -*- coding: utf-8 -*-
import scrapy


class QuotesRandomSpider(scrapy.Spider):
    name = 'quotes_random'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/random']

    def parse(self, response):
        self.log('************************************************ crawling ...' + response.url)
        yield {
            'author_name': response.css('small.author::text').extract_first(),
            'text': response.css('span.text::text').extract_first(),
            'tags': response.css('a.tag::text').extract_first(),
        }
