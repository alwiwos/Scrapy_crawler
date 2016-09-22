#!/usr/bin/python
# -*- coding:utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
#from StackOverflow.items import StackoverflowItem


#class StackOverflowSpider(Spider):
  #  """爬虫Spider"""
   # name = "StackOverflow"
   # download_delay = 0.01
   # allowed_domains = ["stackoverflow.com"]    #只爬取有stackoverflow.com的url

    #start_urls = [
	#	"http://stackoverflow.com/questions?sort=frequent"
        #第一篇文章地址
    #]
  #  def parse(self, response):
  #      sel = Selector(response)

        #获得文章url和标题
   #     item = StackoverflowItem()
 #       titles = sel.xpath('//h3/a[@class="question-hyperlink"]/text()').extract()
 #       item['question_title'] = [n.encode('utf-8') for n in titles]
 #       urls = sel.xpath('//h3/a[@class="question-hyperlink"]/@href').extract()
 #       item['question_url'] =[("http://stackoverflow.com"+url).encode('utf-8') for url in urls]
 #       yield item

        #获得下一页文章的url
#      url = sel.xpath('//*[@id="mainbar"]/div[4]/a[@rel="next"]/@href').extract()
 #       url ="http://stackoverflow.com"+url[0]
  #      yield Request(url, callback=self.parse)

     # article_name = sel.xpath('//h1/a[@class="question-hyperlink"]/text()').extract()
     #   item['question_title'] = [n.encode('utf-8') for n in article_name]
   #     article_url = str(response.url)
    #    item['question_url'] = article_url.encode('utf-8')
    #   tags = sel.xpath('//*[@class="post-taglist"]/a/text()').extract()
    #    item['Tag'] = [n.encode('utf-8') for n in tags]
     #   yield item

    #    urls = sel.xpath('//a[@class="question-hyperlink"]/@href').extract()
    #    for url in urls:
            #           print url
      #      url = "http://stackoverflow.com" + url
#            yield Request(url, callback=self.parse)



import scrapy
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader, Identity
from StackOverflow.items import MeizituItem


class MeiziSpider(scrapy.Spider):
    name = "StackOverflow"
    allowed_domains = ["meizitu.com"]
    start_urls = (
        'http://www.meizitu.com/',
    )

    def parse(self, response):
        # sel是页面源代码，载入scrapy.selector
        sel = Selector(response)
        # 每个连接，用@href属性
        for link in sel.xpath('//h2/a/@href').extract():
            # 请求=Request(连接，parese_item)
            request = scrapy.Request(link, callback=self.parse_item)
            yield request  # 返回请求
        # 获取页码集合
        pages = sel.xpath('//*[@id="wp_page_numbers"]/ul/li/a/@href').extract()
        print('pages: %s' % pages)  # 打印页码
        if len(pages) > 2:  # 如果页码集合>2
            page_link = pages[-2]  # 图片连接=读取页码集合的倒数第二个页码
            page_link = page_link.replace('/a/', '')  # 图片连接=page_link（a替换成空）
            request = scrapy.Request('http://www.meizitu.com/a/%s' % page_link, callback=self.parse)
            yield request  # 返回请求

    def parse_item(self, response):
        # l=用ItemLoader载入MeizituItem()
        l = ItemLoader(item=MeizituItem(), response=response)
        # 名字
        l.add_xpath('name', '//h2/a/text()')
        # 标签
        l.add_xpath('tags', "//div[@id='maincontent']/div[@class='postmeta  clearfix']/div[@class='metaRight']/p")
        # 图片连接
        l.add_xpath('image_urls', "//div[@id='picture']/p/img/@src", Identity())
        # url
        l.add_value('url', response.url)

        return l.load_item()