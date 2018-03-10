# -*- coding: utf-8 -*-
import scrapy


class QuotesFormRequestSpider(scrapy.Spider):
    name = 'quotes_form_request'
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        self.log('************************************************ crawling ...' + response.url)
        # extract CSRF_TOKEN
        csrf_token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        # dict with form data
        form_data = {
            'csrf_token': csrf_token,
            'username': 'abc',
            'password': '123'
        }
        # post requests
        yield scrapy.FormRequest(
            url=self.login_url,
            formdata=form_data,
            callback=self.parse_quotes
        )

    def parse_quotes(self, response):
        for quote in response.css('div.quote'):
            yield {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract_first(),
            }
