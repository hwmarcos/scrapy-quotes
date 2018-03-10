# -*- coding: utf-8 -*-
import scrapy


class QuotesPaginationSpider(scrapy.Spider):
    name = 'quotes_pagination'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.log('************************************************ crawling ...' + response.url)
        i = 1
        for quote in response.css('div.quote'):
            self.log(i)
            yield {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract_first(),
            }
            i += 1
        next_page = response.css('li.next > a::attr(href)').extract_first()
        if (next_page):
            next_page_url = response.urljoin(next_page)
            self.log('************************************************ next page =>  ...' + next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)
