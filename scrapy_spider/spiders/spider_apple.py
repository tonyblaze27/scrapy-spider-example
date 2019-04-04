# -*- coding: utf-8 -*-
import scrapy
from scrapy_spider.items import QuoteItem

class AppleSpiderSpider(scrapy.Spider):
    name = 'apple_spider'
    allowed_domains = ['apple.com']
    start_urls = ['https://www.apple.com/retail/storelist/']

    def parse(self, response):
        quotes = response.xpath("//div[@class='toggle']")
        for quote in quotes:
            text = quote.xpath(
                ".//span[@class='text']/text()").extract_first()
            author = quote.xpath(
                ".//small//text()").extract_first()

            item = QuoteItem()
            item["toggle"] = text
            item["author"] = author

            yield item

        next_page_url = response.xpath("//li[@class='next']//a/@href").extract_first()
        if next_page_url:
            absolute_next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(absolute_next_page_url)
