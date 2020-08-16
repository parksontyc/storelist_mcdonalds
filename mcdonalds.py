from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import csv

store_name = []
store_addr = []

city = ["基隆", "台北市", "新北", "桃園", "新竹", "苗栗", "台中", "彰化", "雲林", "南投", "嘉義", "台南", "高雄", "屏東", "台東", "花蓮", "宜蘭"]

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications":2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.implicitly_wait(10)    
url = "https://www.mcdonalds.com.tw/tw/ch/index.html"
driver.get(url)
#driver.find_element_by_xpath("//*[@class='closeBtn close1']").click()    #處理跳出框
#driver.find_element_by_xpath("//*[@class='closeBtn close2']").click()    #處理跳出框

driver.find_element_by_xpath("//*[@id='noflyout_link_8']").click()      #搜餐廳
time.sleep(5)

login_frame = driver.find_element_by_xpath("//iframe[@id='frameiframeherosectionpar']")
driver.switch_to_frame(login_frame)
for i in city:
    driver.find_element_by_tag_name("input").clear()
    time.sleep(1)
    driver.find_element_by_tag_name("input").send_keys('%s' %i)
    print('目前城市:%s' %i)
    driver.find_element_by_link_text('立即搜尋').click()
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "noLocFoundMsg")))
    #driver.switch_to_default_content()
    #item_frame = driver.find_element_by_xpath("//iframe[@id='inneriframe']")
    #driver.switch_to_frame(item_frame)
    time.sleep(10)
    page = 1
    soup = BeautifulSoup(driver.page_source.replace("\n", "").strip(), "html.parser")
    count = soup.find('div', id='pagination').td.find_next().text[2:]
    count = int(count)
    print('page : %s' %count)
    print('目前頁數:%s' %page)
    all_item = soup.find_all("tr", class_="padding10")
    for name in all_item:
        store_name.append(name.find('td', {"align":"center"}).text)
        print(store_name)
    for addr in all_item:
        store_addr.append(addr.h3.text.replace("\n", "").strip()[6:])
        print(store_addr)
    for page in range(1, count):
        if page < count:
            page += 1
            driver.find_element_by_xpath("//*[@id='pagination']/table/tbody/tr/td[3]/a").click()
            time.sleep(5)
            print('目前頁數:%s' %page)
            soup = BeautifulSoup(driver.page_source.replace("\n", "").strip(), "html.parser")
            all_item = soup.find_all("tr", class_="padding10")
            for name in all_item:
                store_name.append(name.find('td', {"align":"center"}).text)
                print(store_name)
            for addr in all_item:
                store_addr.append(addr.h3.text.replace("\n", "").strip()[6:])
                print(store_addr)

time.sleep(2)
driver.close()

with open('storelist_麥當勞.csv', 'w', newline='',  encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    newrow = ['門市名稱', '門市地址']
    csvwriter.writerow(newrow)
    for n in range(0, len(store_name)):
        newrow.clear()
        newrow.append(store_name[n])
        newrow.append(store_addr[n])
        csvwriter.writerow(newrow)


