# -*- coding: utf-8 -*-
import scrapy
import json


class QuotesScrollSpider(scrapy.Spider):
    name = 'quotes_scroll'
    base_url = 'http://quotes.toscrape.com/api/quotes?page={}'
    start_urls = [base_url.format(1)]

    def parse(self, response):
        self.log('************************************************ crawling ...' + response.url)
        data = json.loads(response.text)
        for quote in data['quotes']:
            yield {
                'author_name': quote['author']['name'],
                'text': quote['text'],
                'tags': quote['tags'],
            }
        if data['has_next']:
            next_page = data['page'] + 1
            yield scrapy.Request(
                url=self.base_url.format(next_page),
                callback=self.parse
            )
