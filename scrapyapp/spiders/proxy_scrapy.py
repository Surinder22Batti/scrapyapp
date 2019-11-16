# -*- coding: utf-8 -*-
import scrapy


class ProxyScrapySpider(scrapy.Spider):
    name = 'proxy_scrapy'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/']

    def parse(self, response):
        item_url = "https://stackoverflow.com/questions/4710483/scrapy-and-proxies"
        yield scrapy.Request(url=item_url, callback=self.getProductDetail, meta={'proxy': 'https://159.8.18.178:8600'})
    
    # method to get product detail.
    def getProductDetail(self, response):
        print response.meta
        print "###############################################"
        # products = response.css('.product')
        # if len(products):
        #     for product in products:
        #         # this is for get product url.
        #         product_url = product.xpath(".//div[@class='productDetails']/div/a/@href").extract_first()
        #         if 'http' not in product_url:
        #             product_url = 'https://www.darice.com' + str(product_url)
        #         # this is for get product title.
        #         title = product.xpath(".//meta[@itemprop='name']/@content").extract_first()
        #         # this is for get product image.
        #         image = product.xpath(".//meta[@itemprop='image']/@content").extract_first()
        #         # this is for get product UPC.
        #         product_upc = product.xpath(".//meta[@itemprop='gtin12']/@content").extract_first()
        #         # this is for get product SKU.
        #         product_sku = product.xpath(".//meta[@itemprop='productID']/@content").extract_first()
        #         # this is for get product price.
        #         price = product.xpath(".//div[@class='productPrice']/text()").extract_first()
        #         if price:
        #             price = str(price).lower().strip().replace('your price :', '').strip()

        #         yield {
        #             "URL": product_url,
        #             "title": title,
        #             "upc": product_upc,
        #             "sku": product_sku,
        #             "price": price,
        #         }
        
