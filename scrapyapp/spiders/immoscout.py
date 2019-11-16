# -*- coding: utf-8 -*-
import scrapy
import json
from scrapyapp.items import ImmoscoutItem
import requests

class ImmoscoutSpider(scrapy.Spider):
    name = "immoscout"
    allowed_domains = ["immobilienscout24.de"]
    # start_urls = ['https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin']
    start_urls = ['https://www.immobilienscout24.de/Suche/S-T/Wohnung-Kauf/Nordrhein-Westfalen/Dortmund/-/-/-/EURO-50000,00-150000,00?enteredFrom=result_list']

    # The immoscout search results are stored as json inside their javascript. This makes the parsing very easy.
    # I learned this trick from https://github.com/balzer82/immoscraper/blob/master/immoscraper.ipynb .
    script_xpath = './/script[contains(., "IS24.resultList")]' #JavaScript on search list page
    next_xpath = '//div[@id = "pager"]/div/a/@href' #go to next page

    # def start_requests(self):
    #     yield scrapy.Request(self.url)

    def parse(self, response):
        # print(response.url)
        total_results = response.xpath("//h1[@data-is24-qa='resultlist-headline']/span/text()").extract_first()
        print("Total Results : ",total_results)

        for line in response.xpath(self.script_xpath).extract_first().split('\n'):
            
            if line.strip().startswith('resultListModel'):
                immo_json = line.strip()
                immo_json = json.loads(immo_json[17:-1]) # everything element including #18..(last-1)

                #TODO: On result pages with just a single result resultlistEntry is not a list, but a dictionary.
                #TODO: So extracting data will fail.
                for result in immo_json["searchResponseModel"]["resultlist.resultlist"]["resultlistEntries"][0]["resultlistEntry"]:

                    item = ImmoscoutItem() #define new field if needed here

                    data = result["resultlist.realEstate"]
                    #print("---------------------------------------")
                    #print(data)
                    #print("---------------------------------------")
                    
                    #General Information
                    item['immo_id'] = data['@id']
                    item['title'] = data['title']
                    item['url'] = response.urljoin("/expose/" + str(data['@id']))
                    item['retype'] = data['@xsi.type']
                    # #Adress
                    address = data['address']
                    try:
                        item['address'] = address['city'] + " " + address['street'] + " " + address['houseNumber'] 
                    except:
                        item['address'] = ""

                    if "city" not in address.keys():
                        address['city'] = ""
                    if "street" not in address.keys():
                        address['street'] = ""
                    if "houseNumber" not in address.keys():
                        address['houseNumber'] = ""

                    # item['city'] = address['city']
                    # item['street'] = address['street']
                    # item['housenumber'] = address['houseNumber']
                    if "preciseHouseNumber" in data:
                        item['precisehousenumber'] = address['preciseHouseNumber']
                    else:
                        item['precisehousenumber'] = ""
                    item['zip_code'] = address['postcode']
                    item['district'] = address['quarter']
                    try:
                        item['lat'] = address['wgs84Coordinate']['latitude']
                        item['lng'] = address['wgs84Coordinate']['longitude']
                    except Exception as e:
                        # print(e)
                        item['lat'] = ""
                        item['lng'] = ""
                    # #Additions
                    if "balcony" in data:
                        item["balcony"] = data["balcony"]
                    else:
                        item["balcony"] = ""
                    if "builtInKitchen" in data:
                        item["kitchen"] = data["builtInKitchen"]
                    else:
                        item["kitchen"] = ""
                    if "cellar" in data:
                        item["cellar"] = data["cellar"] 
                    else:
                        item["cellar"] = ""
                    if "companywidecustomerid" in data:
                        item['companywidecustomerid'] = address['companyWideCustomerId']
                    else:
                        item["companywidecustomerid"] = ""
                    # #contactDetails
                    if "contactDetails" in data.keys():
                        contact = data['contactDetails']
                        try:
                            item['contcompany'] = contact['company']
                        except:
                            item['contcompany'] = ''
                        try:
                            item['contname'] = contact['firstname'] + " " + contact["lastname"]
                        except:
                            item['contname'] = ""
                        try:
                            item['contfirstname'] = contact['firstname']
                        except:
                            item['contfirstname'] = ""
                        try:
                            item['contlastname'] = contact['lastname']
                        except:
                            item['contlastname'] = ""
                        try:
                            item['contphonenumber'] = contact['phoneNumber']
                        except:
                            item['contphonenumber'] = ""
                        try:
                            item['contsalutation'] = contact['salutation']
                        except:
                            item['contsalutation'] = ''
                    else:
                        item['contcompany'] = ''
                        item['contname'] = ''
                        item['contfirstname'] = ''
                        item['contlastname'] = ''
                        item['contphonenumber'] = ''
                        item['contsalutation'] = ''
                    # #courtage
                    try:
                        courtage = data['courtage']
                        item['hascourtage'] = courtage['hasCourtage']
                    except:
                        item['hascourtage'] = ''
                    #Additions2
                    try:
                        item['floorplan'] = data['floorplan']
                    except:
                        item['floorplan'] = ''
                    try:
                        item["garden"] = data["garden"]
                    except:
                        item["garden"] = ""
                    try:
                        item["guesttoilet"] = data["guestToilet"]
                    except:
                        item["guesttoilet"] = ""
                    try:
                        item["isbarrierfree"] = data["isBarrierFree"]
                    except:
                        item["isbarrierfree"] = ""
                    try:
                        item["lift"] = data["lift"]
                    except:
                        item["lift"] = ""
                    try:
                        item["listingtype"] = data["listingType"]
                    except:
                        item["listingtype"] = ''
                    try:
                        item["livingspace"] = data["livingSpace"]
                    except:
                        item["livingspace"] = ''
                    try:
                        item["numberofrooms"] = data["numberOfRooms"]
                    except:
                        item["numberofrooms"] = ''
                    # #price
                    # price = data["price"]
                    # item["currency"] = price["currency"]
                    # item["marketingtype"] = price["marketingType"]                    # item["priceintervaltype"] = price["priceIntervalType"]
                    # item["value"] = price["value"]
                    # #Additions3
                    try:
                        item["privateoffer"] = data["privateOffer"]
                    except:
                        item["privateoffer"] = ""
                    try:
                        item["realtorcompanyname"] = data["realtorCompanyName"]
                    except:
                        item["realtorcompanyname"] = ""
                    try:
                        item["realtorlogo"] = data["realtorLogo"]
                    except:
                        item["realtorlogo"] = ""
                    try:
                        item["spotlightlisting"] = data["spotlightListing"]
                    except:
                        item["spotlightlisting"] = ''
                    try:
                        item["streamingvideo"] = data["streamingVideo"]
                    except:
                        item["streamingvideo"] = ''
                    # #titlePicture
                    try:
                        titlePicture = data["titlePicture"]
                        item["creation"] = titlePicture["@creation"]
                    except:
                        item["creation"] = ''

                    #TODO what does calculated price represents?
                    #if "calculatedPrice" in data:
                    #    item["extra_costs"] = (data["calculatedPrice"]["value"] - data["price"]["value"])
                    #else:
                    #    item["extra_costs"] = ""
                    
                    #Additional Calculation
                    #TODO: Price per m^2
                    
                    # #TODO: what is plot area?
                    #if "plotArea" in data:
                    #    item["area"] = data["plotArea"]
                    #else:
                    #    item["area"] = ""

                    try:
                        item['media_count'] = len(data['galleryAttachments']['attachment'])
                    except:
                        item['media_count'] = 0
                    
                    #yield item
                    yield scrapy.Request(url=item['url'], callback=self.parse_property, meta={'item': item})

        next_page_list = response.xpath(self.next_xpath).extract()
        if next_page_list:
            next_page = next_page_list[-1]
            print("Scraping next page", next_page)
            if next_page:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_property(self, response):
        item = response.request.meta['item']
        
        #Broker Commission
        # provision1 = response.xpath("//span[contains(@class, 'broker-commission-value')]/text()").extract_first()
        # provision2 = response.xpath("//span[@class='broker-commission-percentage']")
        # provision1 = soup.find(text=re.compile("Broker commission"))

        #Land Transfer Tax
        # land1 = response.xpath("//span[@class='land-transfer-value font-semibold font-s']")
        # land2 = response.xpath("//span[@class='land-transfer-percentage']")

        #Notary
        # notary1 = response.xpath("//span[@class='notary-costs-value font-semibold font-s']")
        # notary2 = response.xpath("//span[@class='notary-costs-percentage']")

        #Land Registry Entry
        # land1 = response.xpath("//span[@class='entry-land-register-value font-semibold font-s']")
        # land2 = response.xpath("//span[@class='entry-land-register-percentage']")

        try:
            criteriagroup = response.xpath("//dd[@class='is24qa-baujahr grid-item three-fifths']/text()").extract_first()
        except:
            criteriagroup = ""
        
        try:
            objektbeschreibung = response.xpath("//pre[@class='is24qa-objektbeschreibung text-content short-text']/text()").extract_first()
        except:
            objektbeschreibung = ""

        try:    
            sonstiges = response.xpath("//pre[@class='is24qa-sonstiges text-content short-text']/text()").extract_first()
        except:
            sonstiges = ""
            
        item.update({'criteriagroup': criteriagroup})
        item.update({'objektbeschreibung': objektbeschreibung})
        item.update({'sonstiges': sonstiges})
        
        url = 'https://www.immobilienscout24.de/baufinanzierung-api/restapi/api/financing/construction/v1.0/monthlyrate?exposeId={}'.format(item['immo_id'])
        yield scrapy.Request(url=url, callback=self.get_addition_price, meta={'item': item})

    def get_addition_price(self, response):
        item = response.request.meta['item']
        res = requests.get(response.url)
        data = res.json()
        provision1 = data['additionalCosts']['brokerCommission']
        provision2 = data['additionalCosts']['brokerCommissionPercentage']
        land_transfer1 = data['additionalCosts']['landTransfer'] 
        land_transfer2 = data['additionalCosts']['landTransferPercentage'] 
        notary1 = data['additionalCosts']['notaryCosts'] 
        notary2 = data['additionalCosts']['notaryCostsPercentage']
        entry_land1 = data['additionalCosts']['entryLandRegister'] 
        entry_land2 = data['additionalCosts']['entryLandRegisterPercentage']
        
        item.update({'provision1': provision1})
        item.update({'provision2': provision2})
        item.update({'land_transfer1': land_transfer1 / 1000})
        item.update({'land_transfer2': land_transfer2})
        item.update({'notary1': notary1 / 1000})
        item.update({'notary2': notary2})
        item.update({'entry_land1': entry_land1})
        item.update({'entry_land2': entry_land2})
        yield item