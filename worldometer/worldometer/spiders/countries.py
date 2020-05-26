# -*- coding: utf-8 -*-
import scrapy
import logging


class CountriesSpider(scrapy.Spider):
    name = 'countries'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']



    def parse(self, response):
        countries = response.xpath("//td/a")
        for country in countries:
            country_name = country.xpath(".//text()").get()
            country_link = country.xpath(".//@href").get()

            #following code block will return the country name and href attribute value
            # yield {
            #     'country_name': country_name,
            #     'country_link': country_link
            # }

            #Sample Output in the shell
            #{'country_name': 'Montserrat', 'country_link': '/world-population/montserrat-population/'}

            #other way to achieve this using abs url
            # absolute_url = response.urljoin(link)

            yield response.follow(url=country_link,callback=self.parse_country, meta={'country_name': country_name})


    def parse_country(self,response):
        name = response.request.meta['country_name']
        rows = response.xpath("(//table[@class ='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")
        for row in rows:
            year = row.xpath(".//td[1]/text()").get()
            population_count = row.xpath(".//td[2]/strong/text()").get()

            yield{
                'country_name': name,
                'year': year,
                'population_count': population_count
            }