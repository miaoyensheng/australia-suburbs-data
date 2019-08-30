# -*- coding: utf-8 -*-
import scrapy

class NewSouthWalesSpider(scrapy.Spider):
    name = 'new_south_wales'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Sydney_suburbs']

    def parse(self, response):
        suburbs = response.css('.mw-parser-output h2 + p a ::attr(title)').extract()     
        urls = response.css('.mw-parser-output h2 + p a ::attr(href)').extract()     

        for i in range(len(urls)):
            callback_url = 'https://'+self.allowed_domains[0] + urls[i]
            yield scrapy.Request(url=callback_url, callback = self.parse_listing, meta={'suburb':suburbs[i]}, dont_filter=True)

    def parse_listing(self, response):

        suburb = response.meta['suburb']

        coordinates = response.xpath('//*[contains(@class, "geo")]/text()').extract()[3]
        coordinates = coordinates.split(";")

        latitude = coordinates[0].strip()
        longitude = coordinates[1].strip()

        postcode = response.xpath('//th[a[@href="/wiki/Postcodes_in_Australia"]]/following-sibling::td/text()').extract()

        local_government_area = response.xpath('//th[a[@href="/wiki/Local_government_areas_of_New_South_Wales"]]/following-sibling::td/a/text()').extract()

        yield {
            'suburb': suburb,
            'latitude': latitude,
            'longitude': longitude,
            'postcode': postcode,
            'local_government_area': local_government_area
        }

