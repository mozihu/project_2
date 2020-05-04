# -*- coding: utf-8 -*-
import scrapy
import re
import time
import datetime


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['www.tripadvisor.cn']
    start_urls = [
        'https://www.tripadvisor.cn/Restaurants-g297415-oa{}-Shenzhen_Guangdong.html'.format(10 * num) for num in range(0, 10, 3)]

    def parse(self, response):
        selectors = response.xpath('//div[@class="wQjYiB7z"]')
        # link = selectors[29].xpath('./span/a/@href').get()
        # url = response.urljoin(link)
        # yield scrapy.Request(url, callback=self.parse_info)

        for link in selectors:
            # print(f"{''.join(link.xpath('./span/a/text()').getall())}")
            link = selectors.xpath('./span/a/@href').get()
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parse_info)

        # next_page = response.xpath('//div[@class="unified pagination js_pageLinks"]/a[2]/@href').get()
        # if next_page:
        #     next_url = response.urljoin(next_page)
        #     print(next_url)
        #     yield scrapy.Request(next_url, callback=self.parse)

    def parse_info(self, response):
        selectors = response.xpath('//div[@class="ui_column is-9"]')
        restaurant = response.xpath('//h1[@class="ui_header h1"]/text()').get()
        current_page = response.xpath(
            '//a[contains(@class, "pageNum first current ") or contains(@class, "pageNum current ") or contains(@class, "pageNum last current ")]/text()').get()
        if current_page:
            print(f"{restaurant} 第{current_page}页...")
        else:
            print(f"{restaurant} 第1页...")

        for selector in selectors:
            date = selector.xpath('./span[2]/@title').get()
            ymd = re.findall('\d+', date)
            now = datetime.date.today()
            diff = now.__sub__(datetime.date(
                int(ymd[0]), int(ymd[1]), int(ymd[2])))

            if diff.days < 1:
                date = '-'.join(ymd)
                rating = selector.xpath('./span[1]/@class').get()[-2]
                title = selector.xpath('./div[1]/a/span/text()').get()
                review = selector.xpath('./div[2]//div[1]/p/text()').get()
                items = {
                    'date': date,
                    'rating': rating,
                    'title': title,
                    'review': review,
                }
                yield items

                next_page = response.xpath(
                    '//div[@class="unified ui_pagination "]/a[2]/@href').get()
                if next_page:
                    next_url = response.urljoin(next_page)
                    print(next_url)
                    yield scrapy.Request(next_url, callback=self.parse_info)
            else:
                break
