# -*- coding: utf-8 -*-
import scrapy


class TruliaSpider(scrapy.Spider):
    name = 'trulia'
    allowed_domains = ['trulia.com']
    start_urls = ['https://trulia.com/']

    def parse(self, response):
        # This have google captcha to prevent automation.
        print("UUUU : ",response.url)
        search_box = response.xpath("//input[@id='homepageSearchBoxTextInput']/@value").extract_first()
        print("search_box : ",search_box)
