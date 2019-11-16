# -*- coding: utf-8 -*-
import scrapy
import json


class FlipkartSpider(scrapy.Spider):
    name = 'flipkart'
    # allowed_domains = ['flipkart.com']
    start_urls = ['https://www.flipkart.com/']

    def parse(self, response):
        # url1 = input("Enter url : ")
        # print("url : ",url)
        links = [
            "https://www.flipkart.com/search?q=books&sid=bks&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_2_4&otracker1=AS_QueryStore_OrganicAutoSuggest_2_4&as-pos=2&as-type=RECENT&as-searchtext=Book&p%5B%5D=facets.serviceability%5B%5D%3Dtrue&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove",
        ]

        for link in links:
            yield scrapy.Request(url=link, callback=self.getProductsLinks)

    def getProductsLinks(self, response):
        products = response.xpath("//a[@class='Zhf2z-']/@href").extract()
        print "Total : ",len(products)
        
        if len(products):
            for product in products:
                if "http" not in product:
                    product = "https://www.flipkart.com" + str(product)
                product_url = product
                yield scrapy.Request(url=product_url, callback=self.getProductDetail)
                break
        else:
            print "No products found."

    def getProductDetail(self, response):
        import json
        json_data = response.xpath("//script[@id='jsonLD']/text()").extract_first()
        print("json_datajson_datajson_datajson_data : before ")
        print(response.url)
        # print(json_data)
        # print(json.loads(str(json_data.encode('utf-8'))))
        if json_data:
            json_data1 = dict(json.loads(str(json_data.encode('utf-8')).strip())[0])
            json_data2 = dict(json.loads(str(json_data.encode('utf-8')).strip())[1])
            title = json_data1['name']
            stars = json_data1['aggregateRating']['ratingValue']
            reviews = json_data1['aggregateRating']['reviewCount']
            price = json_data2['workExample'][0]['potentialAction']['expectsAcceptanceOf']['price']
            priceCurrency = json_data2['workExample'][0]['potentialAction']['expectsAcceptanceOf']['priceCurrency']
            asin = json_data2['workExample'][0]['isbn']
            published_date = json_data2['workExample'][0]['datePublished']
        else:
            title = response.xpath("//span[@class='_35KyD6']/text()").extract_first()
            if title:
                title = str(title).strip()
            price = response.xpath("//div[@class='_1vC4OE _3qQ9m1']/text()").extract_first()
            priceCurrency = "INR"
            asin = response.xpath("//span[@id='fitRecommendationsSection']/@data-asin").extract_first()
            stars = response.xpath("//div[@class='hGSR34 _2beYZw']/text()").extract_first()
            if stars:
                stars = stars.strip().split()[0].strip()
                stars = int(stars)
            reviews = response.xpath("//div[@class='swINJg _3nrCtb']/text()").extract_first()
            published_date = response.xpath("//span[contains(text(), 'Date first listed on Amazon:')]/following-sibling::*/text()").extract_first()
        
        desc = response.xpath("//div[@class='_3la3Fn']/text()").extract_first()
        print "title : ",title
        print "price : ",price
        print "priceCurrency : ",priceCurrency
        print "stars : ",stars
        print "asin : ",asin
        print "published_date : ",published_date
        print "reviews : ",reviews
        print "desc : ",desc
        print '#'*100
        
