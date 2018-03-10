# -*- coding: utf-8 -*-
import scrapy


class QuotesDetailsPageSpider(scrapy.Spider):
    name = 'quotes_details_page'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        self.log('************************************************ crawling ...' + response.url)
        urls = response.css('div.quote > span > a::attr(href)').extract();
        for url in urls:
            url_base = response.urljoin(url)
            yield scrapy.Request(
                url=url_base,
                callback=self.parse_details
            )
        # follow pagination link
        next_page = response.css('li.next > a::attr(href)').extract_first()
        if (next_page):
            next_page_url = response.urljoin(next_page)
            self.log('************************************************ next page =>  ...' + next_page_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_details(self, response):
        yield {
            'name': response.css('h3.author-title::text').extract_first(),
            'birthday': response.css('span.author-born-date::text').extract_first(),
        }
