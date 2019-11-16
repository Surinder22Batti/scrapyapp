# -*- coding: utf-8 -*-
import scrapy

class AmazonNewSpider(scrapy.Spider):
    name = 'amazon_new'
    # allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/gp/bestsellers']

    def parse(self, response):
        links = response.xpath("//ul[@id='zg_browseRoot']/ul/li")
        print("links : ",len(links))
        if len(links):
            for link in links:
                link = link.xpath("./a/@href").extract_first()
                yield scrapy.Request(url=link, callback=self.getProductsByLink)
                break
        print("#"*200)
        
    def getProductsByLink(self, response):
        page_title = response.xpath("//div[@id='zg-right-col']/h1/span/text()").extract_first()
        page_links = response.xpath("//ul[@id='zg_browseRoot']/ul/ul/li")
        print(len(page_links))
        if len(page_links):
            for page_link in page_links:
                page_link = page_link.xpath("./a/@href").extract_first()
                yield scrapy.Request(url=page_link, callback=self.getProducts)
                # break
        
        print("F"*50)

    def getProducts(self, response):
        print("Going to get product:")
        products = response.xpath("//ol[@id='zg-ordered-list']/li")
        print("products : ",len(products))
        if len(products):
            for product in products:
                product_link = product.xpath(".//a[@class='a-link-normal']/@href").extract_first()
                if 'http' not in product_link:
                    product_link = "https://www.amazon.com" + product_link
                yield scrapy.Request(url=product_link, callback=self.getProductDetail)
                # break
        print("J"*100)

    def getProductDetail(self, response):
        product_detail = {
            'title': None,
            'ASIN': None,
            'author': None,
            'rating': 0,
            'reviews_count': 0,
            'price': 0,
            'publish_date': None,
            'description': None,
            'images': []
        }

        title = response.xpath("//span[@id='productTitle']/text()").extract_first()
        if title:
            product_detail.update({'title': str(title).strip()})

        asin = response.xpath("//input[@id='ASIN']/@value").extract_first()
        if asin:
            product_detail.update({"ASIN": str(asin).strip()})

        author = response.xpath("//a[@id='bylineInfo']/text()").extract_first()
        if author:
            product_detail.update({'author': str(author).strip()})
        
        rating = response.xpath("//span[@id='acrPopover']/@title").extract_first()
        if rating:
            product_detail.update({'rating': float(str(rating).split()[0].strip())})

        reviews_count = response.xpath("//span[@id='acrCustomerReviewText']/text()").extract_first()
        if reviews_count:
            product_detail.update({'reviews_count': str(reviews_count).split()[0].strip()})

        price = response.xpath("//span[@id='priceblock_dealprice']/text()").extract_first()
        if price:
            product_detail.update({"price": price})

        desc_lis = response.xpath("//div[@id='feature-bullets']/ul/li")
        product_des = ""
        if len(desc_lis):
            for li in desc_lis:
                li = li.xpath(".//text()").extract_first()
                if li:
                    li = str(li).strip() + "\n"
                    product_des += li
        product_detail.update({"description": product_des})

        images = response.xpath("//div[@id='altImages']/ul/li")
        product_images = []
        if len(images):
            for image in images:
                image = image.xpath(".//img/@src").extract_first()
                if image:
                    product_images.append(image)
        product_detail.update({"images": product_images})
        
        publish_date = response.xpath("//tr[@class='date-first-available']/td")
        if publish_date:
            publish_date = publish_date[-1].xpath(".//text()").extract_first()
        product_detail.update({"publish_date": publish_date})
        print(product_detail)
        print("K"*100)