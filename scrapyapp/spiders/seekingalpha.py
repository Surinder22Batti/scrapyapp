# -*- coding: utf-8 -*-
import scrapy


class SeekingalphaSpider(scrapy.Spider):
    name = 'seekingalpha'
    # allowed_domains = ['https://seekingalpha.com']
    # start_urls = ['https://seekingalpha.com/']
    start_urls = ['https://seekingalpha.com/article/2-mexico-holds-rates-for-4th-month-as-inflation-slows']

    def parse(self, response):
        title = response.xpath("//h1[@itemprop='headline']/text()").extract_first()
        print(title)
        print("#"*100)
