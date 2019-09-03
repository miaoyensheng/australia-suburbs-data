# -*- coding: utf-8 -*-
import scrapy


class QueenslandSpider(scrapy.Spider):
    name = 'queensland'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Brisbane_suburbs']

    def parse(self, response):
        suburbs = response.xpath('//h3[span[@class="mw-editsection"]]/following-sibling::p/a/text()').extract()    
        urls = response.xpath('//h3[span[@class="mw-editsection"]]/following-sibling::p/a/@href').extract()  

        for i in range(len(urls)):
            callback_url = 'https://'+self.allowed_domains[0] + urls[i]
            yield scrapy.Request(url=callback_url, callback = self.parse_listing, meta={'suburb':suburbs[i]}, dont_filter=True)

    def parse_listing(self, response):

        suburb = response.meta['suburb']

        try:
            coordinates = response.xpath('//*[contains(@class, "geo")]/text()').extract()[3]
            coordinates = coordinates.split(";")

            latitude = coordinates[0].strip()
            longitude = coordinates[1].strip()
        except:
            latitude = None
            longitude = None

        try:
            postcode = response.xpath('//th[a[@href="/wiki/Postcodes_in_Australia"]]/following-sibling::td/text()').extract()
        except:
            postcode = None

        try:
            local_government_area = response.xpath('//th[a[@href="/wiki/Local_government_areas_of_Queensland"]]/following-sibling::td/a/text()').extract()
        except:
            postcode = None

        yield {
            'suburb': suburb,
            'latitude': latitude,
            'longitude': longitude,
            'postcode': postcode,
            'local_government_area': local_government_area
        }