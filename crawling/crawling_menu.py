import sys
from selenium import webdriver
import time
import openpyxl
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

univ_addr_list = [
    # '서울특별시 마포구 상수동 와우산로 94',
    '서울특별시 관악구 신림동 산 56-1 서울대학교',
    # '경기도 수원시 장안구 율천동 서부로 2066',
    # '서울특별시 서대문구 대현동 11-1 이화여자대학교',
    # '서울특별시 동대문구 이문로 107',
    # '경기도 수원시 영통구 광교산로 154-42',
    # '서울특별시 성북구 안암로 145',
    # '서울특별시 성동구 사근동 110 한양대학교',
    # '서울특별시 동작구 흑석동 211-32 중앙대학교',
    # '경기도 용인시 처인구 모현읍 외대로 81',
    # '서울특별시 용산구 청파동2가 53-12 숙명여자대학교',
    # '서울특별시 성북구 보문로 34다길 2',
    # '서울특별시 광진구 능동로 209',
    # '경기도 용인시 기흥구 덕영대로 1732',
    # '경기도 성남시 수정구 성남대로 1342',
]

x = "서울대"
wb = openpyxl.Workbook()
sheet = wb.active

sheet.title = f"요기요_{x}"
options = Options()

# Chromedriver 경로 설정
driver = webdriver.Chrome(executable_path="C:\\Users\KSH\dev\chromedriver", chrome_options=options)
driver.get("https://www.yogiyo.co.kr/mobile/#/")
driver.set_window_size(1600, 1000)

# 대학 리스트 반복
for univ_addr in univ_addr_list:
    search = driver.find_element_by_css_selector("div#search input.form-control")
    search.click()
    time.sleep(1)
    driver.find_element_by_css_selector(
        "button.btn-search-location-cancel.btn-search-location.btn.btn-default > span").click()
    time.sleep(1)
    search.send_keys(univ_addr)
    driver.find_element_by_css_selector("button.btn.btn-default.ico-pick").click()

    time.sleep(1)
    SCROLL_PAUSE_TIME = 0.5
    body = driver.find_element_by_css_selector('body')

    for i in range(5, 10):
        try:

            # excel 시트에 인덱스 추가 (카테고리마다 구분되게)
            index = ['store_url', 'logo', 'title', 'star', 'min_price', 'del_time', 'review', 'univ_id', 'cat_name']
            sheet.append(index)

            # 카테고리 선택 후 리뷰많은순으로 선택
            driver.find_element_by_css_selector(f'div#category ul li:nth-child({i})').click()
            category = driver.find_element_by_css_selector(f'div#category ul li:nth-child({i})').text
            order = driver.find_element_by_css_selector('select.form-control')
            selector = Select(order)
            selector.select_by_value('review_count')
            time.sleep(1)

            # 페이지 맨 밑까지 스크롤다운
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            containers = driver.find_elements_by_css_selector('div.item.clearfix')

            # 가게 개수에 따라 다르게 크롤링 (100개 기준)
            print(len(containers))
            if len(containers) > 100:
                con = 110
            else:
                con = len(containers)

            for c in range(con):
                try:
                    time.sleep(1)

                    last_height = driver.execute_script("return document.body.scrollHeight")

                    while True:
                        # Scroll down to bottom
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                        # Wait to load page
                        time.sleep(SCROLL_PAUSE_TIME)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height

                    time.sleep(1)

                    # 가게 상세 페이지 URL 크롤링
                    container = driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[{c + 2}]/div')
                    driver.execute_script("arguments[0].click();", container)

                    time.sleep(1)
                    link = driver.current_url
                    time.sleep(0.5)
                    driver.back()
                    time.sleep(1)

                    last_height = driver.execute_script("return document.body.scrollHeight")

                    while True:
                        # Scroll down to bottom
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                        # Wait to load page
                        time.sleep(SCROLL_PAUSE_TIME)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script("return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height

                    time.sleep(1)

                    # 가게 상세정보 크롤링
                    raw_image_url = driver.find_element_by_css_selector(
                        f'#content > div > div.restaurant-list > div:nth-child({c + 2}) > div > table > tbody > tr > td:nth-child(1) > div:nth-child(1)').get_attribute(
                        'style').split('\"')[1]
                    image_url = 'https://www.yogiyo.co.kr' + raw_image_url
                    title = driver.find_element_by_css_selector(
                        f'#content > div > div.restaurant-list > div:nth-child({c + 2}) > div > table > tbody > tr > td:nth-child(2) > div > div.restaurant-name.ng-binding').text
                    star = driver.find_element_by_css_selector(
                        f'#content > div > div.restaurant-list > div:nth-child({c + 2}) > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(1) > span').text
                    min_price = driver.find_element_by_css_selector(
                        f'#content > div > div.restaurant-list > div:nth-child({c + 2}) > div > table > tbody > tr > td:nth-child(2) > div > ul > li.min-price.ng-binding').text
                    del_time = driver.find_element_by_css_selector(
                        f'#content > div > div.restaurant-list > div:nth-child({c + 2}) > div > table > tbody > tr > td:nth-child(2) > div > ul > li.delivery-time.ng-binding').text
                    review_num = driver.find_element_by_css_selector(
                        f'#content > div > div.restaurant-list > div:nth-child({c + 2}) > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(2)').text[
                                 3:]

                    print(link, image_url, title, star, min_price, del_time, review_num)
                    item = [link, image_url, title, star, min_price, del_time, review_num]
                    sheet.append(item)

                except:
                    print(1)
                    wb.save('./data/yogiyo_경희대_국제_전반.xlsx')
                    print(2)
                    break
        except:
            print(3)
            wb.save('./data/yogiyo_경희대_국제_전반.xlsx')
            print(4)
            sys.exit()
wb.save('./data/yogiyo_경희대_국제_전반.xlsx')
