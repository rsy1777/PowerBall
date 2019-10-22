# -*- coding: utf-8 -*-
import scrapy
import sys
import time
import datetime
from scrapy.spiders import Spider
from scrapy.selector import HtmlXPathSelector
from PowerBall.items import PowerballItem
from scrapy.http import Request
from scrapy.selector import Selector


#3.x 버전은 reload 하지 않아도됨
#reload(sys)
#sys.setdsetdefaultencoding('utf-8') 

class PowerBall_Spider(scrapy.Spider):

    name = "PowerBall"  #spider 이름
    allowed_domains = ["m.nlotto.co.kr"]   #크롤링할 최상위 도메인
    #start_urls = ["http://m.nlotto.co.kr/gameInfo.do?method=powerWinNoList&nowPage=1&searchDate=20181217&calendar=2018-12-17&sortType=num"]  #실제 크롤링할 주소     

    def start_requests(self):
        pageNum = 1
        numdays = 365 * 5
        base = datetime.datetime.today() - datetime.timedelta(days=1)
        date = [base - datetime.timedelta(days=x) for x in range(0, numdays)]

 
        for day in date:            
            for i in range(30, pageNum, -1):
                yield scrapy.Request("http://m.nlotto.co.kr/gameInfo.do?method=powerWinNoList&nowPage={0}&searchDate={1}".format(i, str(day.strftime('%Y%m%d'))),
                                        self.parse)




    def parse(self, response):
        hxs = Selector(response)    #지정된 주소에서 전체 소스코드를 가져옴
        selects =[] #전체 소스코드 중에서 필요한 영역만 잘라내서 담을 리스트
        selects = hxs.xpath('//table[2]/tbody/tr')    #필요한 영역을 잘라서 리스트에 저장
        items = [] #데이터를 Item별로 구별해서 담을 리스트 

        for sel in selects:
            if sel.xpath('td[2]/text()').extract() : 
                item = PowerballItem() #item 객체 선언  
                item['lotteryDay'] = sel.xpath('td[1]/text()').extract() #추첨일
                item['lotteryCount'] = sel.xpath('td[2]/text()').extract() #추첨 회차
                item['lotteryNo'] = sel.xpath('normalize-space(td[3]/script)').extract() #추첨번호
                item['lotteryPowerBall'] = sel.xpath('td[4]/img/@src').extract() #파워볼
                items.append(item) #Item 1개 세트를 리스트에 담음
                
                
                print(item['lotteryCount'])

        return items