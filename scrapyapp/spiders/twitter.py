# -*- coding: utf-8 -*-
import scrapy


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    allowed_domains = ['www.twitter.com']
    start_urls = ['https://twitter.com/search?f=tweets&vertical=default&q=app%20developer&src=tyah']

    def parse(self, response):
        # link = "https://twitter.com/search?f=tweets&vertical=default&q=app%20developer&src=tyah"
        # link = response.urljoin("/search?f=tweets&vertical=default&q=app%20developer&src=tyah")
        # yield scrapy.Request(
        #     url=link,
        #     meta = {
        #           'dont_redirect': True,
        #           'handle_httpstatus_list': [302]
        #         },
        #     callback=self.getPosts)
        print "WWWWWWWWWWWWWWWWW"
        print response.url
        posts = response.xpath("//div[@class='SidebarFilterModule-header']").extract()
        print "Total : "
        print posts

    def getPosts(self, response):
        print "rrrrrrrrrrrrrrr"
        print "link : ",response.url
        posts = response.xpath("//article").extract_first()
        print "Total : "
        print posts
