# -*- coding: utf-8 -*-
import scrapy


class HomedepotSpider(scrapy.Spider):
    name = 'homedepot'
    allowed_domains = ['homedepot.com']
    # start_urls = ['https://www.homedepot.com/s/books?NCNI-5']
    start_urls = ["https://www.homedepot.com/b/Appliances-Washers-Dryers-Washing-Machines-Front-Load-Washers/N-5yc1vZc3pj"]

    def parse(self, response):
        total = response.xpath("//span[@id='allProdCount']/text()").extract_first()
        print "Total : ",total
        products = response.xpath("//div[@class='pod-plp__description js-podclick-analytics']/a/@href").extract()
        print "products : ",len(products)
        if products:
            for product in products:
                if "http" not in product:
                    product = "https://www.homedepot.com" + product
                yield scrapy.Request(url=product, callback=self.getProductDetail)
                # break
        
        # while True:
        #     try:
        #         next_page = response.xpath("//a[@title='Next']/@href").extract_first()
        #         print "next_page : ",next_page
        #         if next_page:
        #             if "http" not in next_page:
        #                 next_page = "https://www.homedepot.com" + next_page
        #             # yield scrapy.Request(url=next_page, self.parse())
        #             print next_page
        #         else:
        #             break
        #     except:
        #         break


    def getProductDetail(self, response):
        print "Ging to get product detail : "
        
        title = response.xpath("//h1[@class='product-title__title']/text()").extract_first()
        if title:
            title = str(title).strip()
        price = response.xpath("//span[@class='price__dollars']/text()").extract_first()
        if price:
            price = str(price).strip()
        priceCurrency = "$"
        currency = response.xpath("//span[@class='price__currency']/text()").extract_first()
        image = response.xpath("//img[@id='mainImage']/@src").extract_first()
        desc = ""
        descs = response.xpath("//div[@class='buybox__salient-points hidden-xs-down']/ul/li/text()").extract()
        if descs:
            for d in descs:
                d = d + "\n"
                desc += d
        
        specification_cont = response.xpath("//div[@class='kpf-appliances__specs']")[-1]
        specifications = specification_cont.xpath(".//div[@class='kpf-appliances__spec-block']")
        # print "specifications : ",len(specifications)
        spec_data = {}
        if specifications:
            for specification in specifications:
                name = specification.xpath(".//div[@class='kpf-appliances__spec-name']/text()").extract_first()
                if name:
                    name = str(name).strip()
                value = specification.xpath(".//div[@class='kpf-appliances__spec-value']/text()").extract_first()
                if value:
                    value = str(value).strip()
                spec_data.update({name: value})
        print "title : ",title
        print "price : ",price
        print "image : ",image
        print "description : ",desc
        print "spec_data : ",spec_data
        print '#'*100
