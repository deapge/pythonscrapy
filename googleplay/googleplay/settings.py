# Scrapy settings for googleplay project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'googleplay'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['googleplay.spiders']
NEWSPIDER_MODULE = 'googleplay.spiders'
DEFAULT_ITEM_CLASS = 'googleplay.items.GoogleplayItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

