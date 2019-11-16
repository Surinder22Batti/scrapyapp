# -*- coding: utf-8 -*-
import scrapy
import xlrd


class IcgcSpider(scrapy.Spider):
    name = 'icgc'
    # allowed_domains = ['https://www.ic.gc.ca']
    start_urls = ['https://www.ic.gc.ca/']

    def parse(self, response):
        # print(response.body)

        file_path = "/home/gc14/Downloads/sample1.xlsx"
        wb = xlrd.open_workbook(file_path) 
        sheet = wb.sheet_by_index(0) 
        
        # For row 0 and column 0 
        # sheet.cell_value(0, 0)
        for i in range(1, sheet.nrows):
            link = sheet.cell_value(i, 0)
            yield scrapy.Request(url=link, callback=self.getItemDetail)

    def getItemDetail(self, response):
        title = response.xpath("//h2[@class='panel-title']/text()").extract_first()
        # print("title : ",title)
        yield {
            'title': title
        }
        # print("#"*100)
