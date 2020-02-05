from selenium import webdriver
import time
import openpyxl
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

x = "홍익대학교"
y = '서울 마포구 와우산로 94'
wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = f"요기요_{x}"
options = Options()

driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)
driver.get("https://www.yogiyo.co.kr/mobile/#/")
driver.set_window_size(1600, 1000)
search = driver.find_element_by_css_selector("div#search input.form-control")
search.click()
time.sleep(1)
driver.find_element_by_css_selector("button.btn-search-location-cancel.btn-search-location.btn.btn-default > span").click()
time.sleep(1)
search.send_keys(y)
driver.find_element_by_css_selector("button.btn.btn-default.ico-pick").click()

time.sleep(1)
SCROLL_PAUSE_TIME = 0.5
body = driver.find_element_by_css_selector('body')
for i in range(5, 15):
    driver.find_element_by_css_selector(f'div#category ul li:nth-child({i})').click()
    category = driver.find_element_by_css_selector(f'div#category ul li:nth-child({i})').text
    print(category)
    order = driver.find_element_by_css_selector('select.form-control')
    selector = Select(order)
    selector.select_by_value('review_count')
    # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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

    for c in range(len(containers)):
        try:
            time.sleep(1)
            # container = driver.find_element_by_css_selector(f'div.item.clearfix:nth-child({c+1})')
            # image = driver.find_elements_by_class_name('logo').screenshot('test.jpg')
            title = driver.find_element_by_css_selector(f'#content > div > div.restaurant-list > div:nth-child({c+2}) > div > table > tbody > tr > td:nth-child(2) > div > div.restaurant-name.ng-binding').text
            star = driver.find_element_by_css_selector(f'#content > div > div.restaurant-list > div:nth-child({c+2}) > div > table > tbody > tr > td:nth-child(2) > div > div.stars > span:nth-child(1) > span').text
            min_price = driver.find_element_by_css_selector(f'#content > div > div.restaurant-list > div:nth-child({c+2}) > div > table > tbody > tr > td:nth-child(2) > div > ul > li.min-price.ng-binding').text
            del_time = driver.find_element_by_css_selector(f'#content > div > div.restaurant-list > div:nth-child({c+2}) > div > table > tbody > tr > td:nth-child(2) > div > ul > li.delivery-time.ng-binding').text
            print(title, star, min_price, del_time)
        except:
            break
        # container.click()
        # time.sleep(1)
        # title = driver.find_element_by_css_selector('span.restaurant-name').text
        # min_price = driver.find_element_by_css_selector('#content > div.restaurant-detail.row.ng-scope > div.col-sm-8 > div.restaurant-info > div.restaurant-content > ul > li:nth-child(2) > span').text
        #
        # print(title)
        # print(min_price)

# sum = 0
# while sum < 5:
#     for i in range(10):
#         if (i % 5) != 4:
#             page = driver.find_elements_by_css_selector("div.pageWrap")[1]
#             page.find_elements_by_css_selector("a")[i % 5].click()
#             time.sleep(1)
#         elif (i % 5) == 4:
#             driver.find_elements_by_css_selector("button.next")[1].click()
#             time.sleep(1)
#
#         container = driver.find_elements_by_css_selector("li.PlaceItem")
#         for j in container:
#             title = j.find_element_by_css_selector("a.link_name").text
#             place = j.find_element_by_css_selector("div.addr p.lot_number").text
#             sheet.append([title, place])
#             print(place)
#         sum += 1

wb.save("yogiyo_1.xlsx")
