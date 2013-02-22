#/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
from os import path,access,R_OK
import re
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

reload(sys)
sys.setdefaultencoding("UTF-8")

class TopSellingNewFreeSpider(BaseSpider):
    name = "TopSellingNewFree"
    allowed_domains = ["play.google.com"]
    start_urls = []
    def __init__(self,start=0):
      #if path.exists(self.filename) and path.isfile(self.filename) and access(self.filename, R_OK):
      #  os.remove(self.filename)
      #self.start_urls = ["https://play.google.com/store/apps/collection/topselling_new_free?start=%s&num=24" % start,
      #                   "https://play.google.com/store/apps/collection/topselling_new_free?start=0&num=24"]
      for i in range(100):
        self.start_urls.append("https://play.google.com/store/apps/collection/topselling_new_free?start="+str(int(i*24)))
      
    rules = (
        #Rule(SgmlLinkExtractor(allow=('example\.com', 'start='), deny=('sort='), restrict_xpaths = '//div[@class="pagination"]'), callback='parse_item'),
        #Rule(SgmlLinkExtractor(allow=('store/apps/collection/topselling_new_free'), callback = 'parse')),
        #Rule(SgmlLinkExtractor(allow=('item\/detail', )), follow = False),
    )
    xmlTemplate = """
        <item>
          <image>%(image)s</image>
          <stars>%(stars)s</stars>
          <title>%(title)s</title>
          <category>%(category)s</category>
          <desc>%(desc)s</desc>
          <link>%(link)s</link>
        </item>
        """
    def parse(self, response):
        xmlstring = '<?xml version="1.0" encoding="UTF-8"?><root>'
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//ul[contains(@class,'snippet-list container-snippet-list')]/li")
        i=0
        for site in sites:
            i +=1
            image = site.select("div/div/div/a[contains(@class,'thumbnail')]/img/@src").extract()[0]
            stars = site.select("div/div/div/div[contains(@class,'ratings')]/@title").extract()
            if len(stars)>0:
              stars = stars[0]
            else:
              stars = 0
            title = site.select("div/div/div/a[contains(@class,'title')]/text()").extract()[0]
            category = site.select("div/div/span[contains(@class,'attribution')]/div/a/text()").extract()[0]
            desc = site.select("div/div/p[contains(@class,'snippet-content')]/text()").extract()[0]
            link = "https://play.google.com/store/apps/details?id=%s" % site.select("@data-docid").extract()[0]
           # print image,stars,title,category,desc,link,'\n'
            #print link
           # print "\n"
            data = {'image':image,'stars':stars,'title':title,'category':category,'desc':desc,'link':link}
            xmlstring += self.xmlTemplate%data
        
        xmlstring += "<size>"+str(i)+"</size></root>"
        start = re.split('start=', response.url)[1]
        filename = 'TopSellingNewFree-'+start+'.xml'
        f = open(filename, 'w+')
        f.write(xmlstring)

