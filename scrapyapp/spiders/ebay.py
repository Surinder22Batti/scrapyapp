# -*- coding: utf-8 -*-
import scrapy


class EbaySpider(scrapy.Spider):
    name = 'ebay'
    allowed_domains = ['ebay.com']
    start_urls = ['https://www.ebay.com/sch/i.html?_from=R40&_trksid=m570.l1313&_nkw=books&_sacat=0']

    def parse(self, response):
        print "GGGGGG : ",response.url
        links = response.xpath("//ul[@class='srp-results srp-list clearfix']/li/div/div/a/@href").extract()
        print("products : ",len(links))
        if links:
            for link in links:
                yield scrapy.Request(url=link, callback=self.getProductDetail)
                break

    def getProductDetail(self, response):
        # import json
        # json_data = response.xpath("//script/text()").extract()[17]
        print("json_datajson_datajson_datajson_data : before ")
        print(response.url)
        
        # # print(json.loads(str(json_data.encode('utf-8'))))
        # if json_data:
        #     json_data = json_data.encode('utf-8')
        #     json_data = json_data.split("vi.cookie.ScreenDetail').init(")[-1]
        #     print json_data
        #     print(type(json_data))
        #     json_data1 = dict(json.loads(str().strip())[0])
        #     json_data2 = dict(json.loads(str(json_data.encode('utf-8')).strip())[1])
        #     title = json_data1['name']
        #     stars = json_data1['aggregateRating']['ratingValue']
        #     reviews = json_data1['aggregateRating']['reviewCount']
        #     price = json_data2['workExample'][0]['potentialAction']['expectsAcceptanceOf']['price']
        #     priceCurrency = json_data2['workExample'][0]['potentialAction']['expectsAcceptanceOf']['priceCurrency']
        #     asin = json_data2['workExample'][0]['isbn']
        #     published_date = json_data2['workExample'][0]['datePublished']
        # else:
        title = response.xpath("//h1[@id='itemTitle']/text()").extract_first()
        if title:
            title = str(title).strip()
        price = response.xpath("//span[@id='prcIsum']/text()").extract_first()
        priceCurrency = "INR"
        image = response.xpath("//img[@id='icImg']/@src").extract_first()
        # asin = response.xpath("//span[@id='fitRecommendationsSection']/@data-asin").extract_first()
        # stars = response.xpath("//div[@class='hGSR34 _2beYZw']/text()").extract_first()
        # if stars:
        #     stars = stars.strip().split()[0].strip()
        #     stars = int(stars)
        # reviews = response.xpath("//div[@class='swINJg _3nrCtb']/text()").extract_first()
        # published_date = response.xpath("//span[contains(text(), 'Date first listed on Amazon:')]/following-sibling::*/text()").extract_first()
        
        # desc = response.xpath("//div[@class='_3la3Fn']/text()").extract_first()
        print "title : ",title
        print "price : ",price
        print "image : ",image
        # print "priceCurrency : ",priceCurrency
        # print "stars : ",stars
        # print "asin : ",asin
        # print "published_date : ",published_date
        # print "reviews : ",reviews
        # print "desc : ",desc
        print '#'*100
    
