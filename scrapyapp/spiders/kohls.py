# -*- coding: utf-8 -*-
import scrapy


class KohlsSpider(scrapy.Spider):
    name = 'kohls'
    allowed_domains = ['kohls.com']
    start_urls = ['http://kohls.com/']

    def parse(self, response):
        pass
