# -*- coding: UTF-8 -*-
__author__ = 'zy'
__time__ = '2020/2/11 19:20'
from scrapy import Selector
from items import CnkispiderItem
from other import OtherSpider
import time,os
import scrapy
import re
from datetime import datetime
from requests_html import HTMLSession
from lxml import etree
from urllib import parse

class ExampleSpider(scrapy.Spider):
    name = 'cnki'
    allowed_domains = ['http://kns.cnki.net']
    start_urls = ['http://kns.cnki.net/KCMS/detail/detail.aspx?DbCode=CJFD&dbname=CJFDLAST2018&filename=CYKX201803010']

    def start_requests(self):
        urls = []
        path=os.path.join(os.getcwd(),'a.txt')
        with open(path, 'r', encoding='utf-8') as f:
            url_ = f.readlines()
            # print(url_)
            for tmp in url_:
                urls.append(tmp[:-1])  # 剔除了\n 换行符
        self.new_urls=[]
        for i in urls:
            # print(i)
            du = OtherSpider.get_detail_url(i)
            print(du)
            self.new_urls.append(du)
        print('@@@@@@@@@@@@@@@@')
        print(self.new_urls)
        for i in self.new_urls:
            yield scrapy.Request(i, callback=self.parse)

    def parse(self, response):

        # response.xpath('//*[@class="entry"]').extract()[0]
        # selector = Selector(text=response.text)
        # print(response)
        # print('######')
        # print(response.xpath('//*[@id="mainArea"]/div[3]/div[1]/h2//text()').extract())
        # print('######')
        try:
            item = CnkispiderItem()

            item['title']  = OtherSpider.clean(response.xpath('//*[@id="mainArea"]/div[3]/div[1]/h2//text()').extract())
            #item['title'] = OtherSpider.clean(response.xpath('//*[@id="mainArea"]/div[3]/div[1]/div[1]/span/a//text()').extract())
            item['author'] = OtherSpider.clean(response.xpath('//*[@id="mainArea"]/div[3]/div[1]/div[1]/span/a//text()').extract())
            item['address'] = OtherSpider.clean(response.xpath('//*[@id="mainArea"]/div[3]/div[1]/div[2]/span/a//text()').extract())
            item['abstract'] = OtherSpider.clean(response.xpath('//span[@id="ChDivSummary"]//text()').extract())
            item['key_word'] = OtherSpider.clean(response.xpath('//label[@id="catalog_KEYWORD"]/../a/text()').extract())
            item['funding'] = OtherSpider.clean(response.xpath('//label[@id="catalog_FUND"]/../a/text()').extract())
            item['publish_time'] = OtherSpider.clean(response.xpath('//a[contains(@onclick,"getKns55NaviLinkIssue")]/text()').extract())
            item['journal']=OtherSpider.clean(response.xpath("//p[@class='title']/a/text()").extract())
            yield item
        except:
            print('error')

# for e in eles:
        #     title_e = e.find('a.title-link', first=True)
        #     if not title_e:
        #         continue
        #
        #     abstract_e = e.find('div.abstract-full', first=True)
        #     if not abstract_e:
        #         continue
        #
        #     href_e = e.find('a:contains(HTML)', first=True)
        #
        #     if not href_e:
        #         href = None
        #     else:
        #         re_href = href_e.attrs['href']
        #         href = f'http://www.mdpi.com{re_href}'
        #
        #     info = dict(title=title_e.text, abstract=abstract_e.text, href=href)
        #
        #     try:
        #         date_e = e.find('div.pubdates', first=True)
        #         m = re.search(r'Received: (.*?) / Revised: (.*?) / Accepted: (.*?) / Published: (.*)', date_e.text)
        #         received = datetime.strptime(m.group(1), '%d %B %Y')
        #         revisied = datetime.strptime(m.group(2), '%d %B %Y')
        #         accepted = datetime.strptime(m.group(3), '%d %B %Y')
        #         published = datetime.strptime(m.group(4), '%d %B %Y')
        #
        #         received = datetime.strftime(received, '%Y-%m-%d')
        #         revisied = datetime.strftime(revisied, '%Y-%m-%d')
        #         accepted = datetime.strftime(accepted, '%Y-%m-%d')
        #         published = datetime.strftime(published, '%Y-%m-%d')
        #         info.update(date=date_e.text, received=received, revisied=revisied, accepted=accepted,
        #                     published=published)
        #     except Exception as e:
        #         pass
        #
        #     items.append(info)
        #