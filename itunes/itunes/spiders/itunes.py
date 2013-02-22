import re
import os
import sys

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from scrapy.http import Request

class ItunesSpider(CrawlSpider):
    name = 'itunes'
    allowed_domains = ['apple.com']
    start_urls = ['https://itunes.apple.com/us/genre/ios-games/id6014?mt=8']

    rules = (
        #Rule(SgmlLinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r'us/app/.+'), callback='parse_item', follow= True),
    )
    
    
    xmlstring = '<?xml version="1.0" encoding="UTF-8"?><root>'
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
    def parse_item(self, response):
        image = stars = title = category = desc = link = ''
        hxs = HtmlXPathSelector(response)
        image = hxs.select("//div[@id='left-stack']/div/a/div/img/@src").extract()[0]
        title = hxs.select("//div[@id='title']/div/h1/text()").extract()[0]
        category = hxs.select("//li[@class='genre']/a/text()").extract()[0]
        desc = hxs.select("//div[@class='product-review']/p").extract()[0]
        data = {'image':image,'stars':stars,'title':title,'category':category,'desc':desc,'link':link}
        self.xmlstring += self.xmlTemplate%data
    
        # http://www.suchkultur.de/blog/suchmaschinen/crawler/web-scraping-mit-dem-scrapy-framework/
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select("//div[@id='selectedcontent']/div/ul/li")
        i=0
        #image = stars = title = category = desc = link = ''
        for site in sites:
            i +=1
            #image = site.select("div/div/div/a[contains(@class,'thumbnail')]/img/@src").extract()[0]
            #stars = ''#site.select("div/div/div/div[contains(@class,'ratings')]/@title").extract()
            #title = site.select("div/div/div/a[contains(@class,'title')]/text()").extract()[0]
            #category = site.select("div/div/span[contains(@class,'attribution')]/div/a/text()").extract()[0]
            #desc = site.select("div/div/p[contains(@class,'snippet-content')]/text()").extract()[0]
            link = site.select("a/@href").extract()[0]
            if i == 1:
              yield Request(link, callback = self.parse_item)
           # print image,stars,title,category,desc,link,'\n'
            #print link
           # print "\n"
            #data = {'image':image,'stars':stars,'title':title,'category':category,'desc':desc,'link':link}
            #self.xmlstring += self.xmlTemplate%data
        
        self.xmlstring += "<size>"+str(i)+"</size></root>"
        filename = 'itunes.xml'
        f = open(filename, 'w')
        f.write(self.xmlstring)
          
