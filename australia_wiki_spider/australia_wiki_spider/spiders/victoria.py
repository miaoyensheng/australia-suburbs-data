# -*- coding: utf-8 -*-
import scrapy


class InfoSpider(scrapy.Spider):
    name = 'victoria'
    allowed_domains = ['en.wikipedia.org/wiki/']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Melbourne_suburbs']

    def parse(self, response):
        data = response.xpath('//*[contains(@class, "wikitable")]/tbody/tr/td//text()').extract()

        for i in range(len(data)):
            if data[i].isnumeric():
                suburb = data[i-1]+ ', Victoria'
                callback_url = 'https://'+self.allowed_domains[0]+suburb.replace(' ', '_')
                postcode = data[i]
                local_government_area = data[i+1]

                yield scrapy.Request(url=callback_url, callback = self.parse_listing, meta={'suburb':suburb, 'postcode':postcode, 'local_government_area':local_government_area},dont_filter=True)

    def parse_listing(self, response):

        suburb = response.meta['suburb']
        postcode = response.meta['postcode']
        local_government_area = response.meta['local_government_area']

        coordinates = response.xpath('//*[contains(@class, "geo")]/text()').extract()[3]
        coordinates = coordinates.split(";")

        latitude = coordinates[0].strip()
        longitude = coordinates[1].strip()

        yield {
            'suburb': suburb,
            'latitude': latitude,
            'longitude': longitude,
            'postcode': postcode,
            'local_government_area': local_government_area
        }