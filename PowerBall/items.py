# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PowerballItem(scrapy.Item):
    lotteryDay = scrapy.Field()        #추첨일
    lotteryCount = scrapy.Field()           #회차
    lotteryNo = scrapy.Field()        #당첨번호
    lotteryPowerBall = scrapy.Field()    #파워볼
 
    
