import pandas as pd
from selenium import webdriver
import time
import openpyxl

from crawling.crawling_menu import options

univ_list = ['가톨릭대학교 성신교정', '가톨릭대학교 성의교정', '건국대학교', '경기대학교 서울캠퍼스', '경희대학교', '고려대학교', '광운대학교', '국민대학교', '덕성여자대학교 쌍문동캠퍼스',
             '덕성여자대학교 종로캠퍼스', '동국대학교', '동덕여자대학교', '명지대학교', '삼육대학교', '상명대학교', '서강대학교', '서경대학교', '서울과학기술대학교',
             '서울대학교 관악캠퍼스', '서울시립대학교', '서울여자대학교', '서울여자대학교', '성균관대학교 인문사회과학캠퍼스', '성균관대학교 자연과학캠퍼스', '성신여자대학교',
             '성신여자대학교 운정그린캠퍼스', '세종대학교', '숙명여자대학교', '숭실대학교', '연세대학교', '이화여자대학교', '중앙대학교', '한국외국어대학교', '한성대학교', '한양대학교',
             '홍익대학교']
x = "서울 마라탕"
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = f"카카오_{x}"

driver = webdriver.Chrome("C:\dev\chromedriver")
driver.get("https://map.kakao.com/")

for univ in univ_list:
    driver.find_element_by_css_selector("div.DimmedLayer").click()
    search = driver.find_element_by_css_selector("input.query.tf_keyword.bg_on")
    search.send_keys(univ)
    driver.find_element_by_css_selector("button.go.ico_search").click()
    time.sleep(1)
    driver.find_element_by_css_selector("div.section.places > a").click()
    driver.find_elements_by_css_selector("ol.Sort a.label")[1].click()
    time.sleep(1)

    container = driver.find_elements_by_css_selector("li.PlaceItem")
    for j in container:
        title = j.find_element_by_css_selector("a.link_name:nth-child(2)").text
        place = j.find_element_by_css_selector("div.addr p:nth-child(1)").text
        print(title, place)
        sheet.append([title, place])

wb.save("./input_update.xlsx")