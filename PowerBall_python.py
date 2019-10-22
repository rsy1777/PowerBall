# -*- coding: UTF-8 -*-

"""
현재 
파이썬 2버젼에서는 정상 작동.
파이썬 3버젼에서는 오류가 일어나는 중. 추후 문제점을 파악 후 이부분 수정해야 할 것 같음.

"""

"""
    @ 데이터 출처: [동행복권-파워볼] https://dhlottery.co.kr/gameInfo.do?method=powerWinNoList
    @ Installed Package: selenium, beautifulsoup4, cfscrape
    @ Requirements : PhantomJS
"""
import os, sys
import re, json, time, cfscrape
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

"""
 * 설정정보
"""

# Driver path
# phantomjsdriver = "/usr/bin/phantomjs"

# 로그인 접속정보
URL = "https://dhlottery.co.kr/user.do?method=login&returnUrl="
PARAMS = {
    'a': 'arri7463',
    'b': 'dkfl7463!'
}

TABLET = "#userId"
TABLEBODY = "#article > div:nth-child(2) > div > form > div > div.inner > fieldset > div.form > input[type=password]:nth-child(2)"
TABLETR = "#article > div:nth-child(2) > div > form > div > div.inner > fieldset > div.form > a"
TARGET_URL = "https://dhlottery.co.kr/gameInfo.do?method=powerWinNoList"

# Sports 고유 아이디
sportsId = "powerball"


"""
 * 공통 함수
"""
# 프로세싱 출력
def printProcessing(msg):
    print("["+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"] "+ msg)

# 당첨번호 얻기
def getNumbers(numbers, powerNum, sumNum):
    regex = re.compile(r"\d+")
    match = regex.search(numbers)
    numbers = match.group()

    i = 0
    sNum = ""
    tmpNumbers = list(numbers)
    newNumbers = []
    totalNum = 0

    for num in tmpNumbers:
        sNum += num
        if i % 2 == 1:
            newNumbers.append(sNum)
            sNum = ""

        i += 1

    newNumbers.append(powerNum)
    newNumbers.append(sumNum)

    return ",".join(newNumbers)

# 브라우저 드라이버 생성
driver = webdriver.PhantomJS(executable_path='/usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')


# 크롤링할 사이트 로그인
printProcessing("Trying login ...")

driver.get(URL)


try:
    # do some webdriver stuff here
    driver.find_element_by_css_selector(TABLET).send_keys(PARAMS['a'])
    driver.find_element_by_css_selector(TABLEBODY).send_keys(PARAMS['b'])
    driver.find_element_by_css_selector(TABLETR).click()
    
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    driver.get_screenshot_as_file('screenshot-%s.png' % now)
except Exception as e:
    print e
    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    driver.get_screenshot_as_file('screenshot-%s.png' % now)

printProcessing("Finished login ...")

"""
 * 메인 프로세스
"""
def main():
    try:
        print("=============================================================")
        print("                 Start PowerBall Crawling                    ")
        print("=============================================================")

        # 웹 수신 정보 읽기
        printProcessing("Searching web data...")

        driver.get(TARGET_URL)
        html = driver.page_source

        printProcessing("Found web data!!")

        # bs4 초기화
        soup = BeautifulSoup(html, 'html.parser')

        # 최근 결과 로우 데이터
        row = soup.select_one("table.tbl_data.tbl_data_col > tbody > tr")

        # 해당 항목 값 검색
        currTurn = row.select("td")[1].text
        nextTurn = str(int(currTurn) + 1)
        next2Turn = str(int(nextTurn) + 1)
        powerNum = row.select("td")[3].text
        sumNum = row.select("td")[4].text
        score = getNumbers(row.select("td")[2].text, powerNum, sumNum)
        
        printProcessing( score + "Found web data!!")
        printProcessing("Found web data!!")

        # 다음회차 신규 게임등록
        printProcessing("Adding new games...")

        printProcessing("Finished to add new games!!")


        # 현재회차 결과처리: 일반볼 (홀/짝)
        printProcessing("Updating game result...")


        printProcessing("Finished updating game result!!")
        print("==============[ Finished PowerBall Crawling ]================")

    except Exception as e:

        # 현재 프로세스 재시작
        executable = sys.executable
        args = sys.argv[:]
        args.insert(0, sys.executable)

        time.sleep(10)
        os.execvp(executable, args)

"""
 * 메인 프로세스 실행
"""
if __name__ == "__main__":
    # 반복적으로 새로고침
    while True:
        # 메인 실행
        main()

        time.sleep(10)
