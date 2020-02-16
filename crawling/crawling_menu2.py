import sys
from selenium import webdriver
import time
import openpyxl
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


def scroll_down():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(0.5)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


univ_addr_list = [
    # '서울특별시 마포구 상수동 와우산로 94',
    # '서울특별시 관악구 신림동 산 56-1 서울대학교',
    # '경기도 수원시 장안구 율천동 서부로 2066',
    # '서울특별시 서대문구 대현동 11-1 이화여자대학교',
    # '서울특별시 동대문구 이문로 107',
    #  '경기도 수원시 영통구 광교산로 154-42',
    # '서울특별시 성북구 안암로 145',
    # '서울특별시 성동구 왕십리로 222',
    # '서울특별시 동작구 흑석동 211-32 중앙대학교',
    # '경기도 용인시 처인구 모현읍 외대로 81',
    # '서울특별시 용산구 청파로47길 100',
    # '서울특별시 성북구 보문로 34다길 2',
    # '서울특별시 광진구 능동로 209',
    '경기도 용인시 기흥구 덕영대로 1732',
    # '경기도 성남시 수정구 성남대로 1342',
]

x = "경희대"
y = '서울특별시 마포구 상수동 와우산로 94'
wb = openpyxl.Workbook()
sheet = wb.active

sheet.title = f"요기요_{x}_new"
options = Options()

driver = webdriver.Chrome(executable_path="C:\\Users\KSH\dev\chromedriver", chrome_options=options)
driver.get("https://www.yogiyo.co.kr/mobile/#/")
driver.set_window_size(1600, 1000)

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

    for i in range(6, 10):
        try:
            # index = ['상세페이지URL', '로고URL', '상호명', '별점', '최소주문금액', '소요시간', '리뷰수']
            index = ['store_url', 'logo', 'title', 'star', 'min_price', 'del_time', 'review', 'univ_id', 'cat_name']

            sheet.append(index)
            driver.find_element_by_css_selector(f'div#category ul li:nth-child({i})').click()
            category = driver.find_element_by_css_selector(f'div#category ul li:nth-child({i})').text
            # sheet = wb.create_sheet(f'{category}')
            order = driver.find_element_by_css_selector('select.form-control')
            selector = Select(order)
            selector.select_by_value('review_count')
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

            containers = driver.find_elements_by_css_selector('div.item.clearfix')
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
                    # container = driver.find_elements_by_css_selector(f'#content > div > div.restaurant-list > div:nth-child({c+2}) > div > table > tbody > tr > td:nth-child(2) > div > div.restaurant-name.ng-binding')
                    # container.click()
                    # container = driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[{c+2}]/div').click()
                    # container.send_keys(Keys.ENTER)

                    container = driver.find_element_by_xpath(f'//*[@id="content"]/div/div[3]/div[{c + 2}]/div')
                    driver.execute_script("arguments[0].click();", container)
                    # print(container.text)
                    # container.click()
                    # container.send_keys('\n')

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
                    wb.save('./data/yogiyo_경희대_new.xlsx')
                    print(2)
                    break
        except:
            print(3)
            wb.save('./data/yogiyo_경희대_new.xlsx')
            print(4)
            sys.exit()
wb.save('./data/yogiyo_경희대_new.xlsx')
