import time, json
import pprint
import pymysql.cursors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

#     from IPython import embed; embed()

def init_driver():
    # driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def getIndex(driver):
    # Connect to the database
    connection = pymysql.connect(host='api.cmivxx.com',
                                 user='frysad',
                                 password='m2JUXxwAeC59HWCn',
                                 db='cm_homep',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    pageLists = []
    driver.get("http://www.frys.com/ads/view-all-store-ads")
    parentElement = driver.find_element_by_class_name("items")
    elementList = parentElement.find_elements_by_class_name("thumbnail_set")
    for index,item in enumerate(elementList):
        pages = elementList[index].find_elements_by_tag_name("a")
        for index,item in enumerate(pages):
            pageLists.append(item)

#### form json data

    adList = []
    mainAdList = []
    for indexA,itemA in enumerate(pageLists):
        adElem = {}
        innerElem = pageLists[index].find_elements_by_tag_name("img")
        adElem["id"] = indexA
        adElem["title"] = innerElem[0].get_attribute("alt")
        adElem["link"] = itemA.get_attribute("href")
        adList.append(adElem)
        # adList[index] = adElem
        # from IPython import embed; embed()

    adListJson = json.dumps(adList)
    # print(adListJson)

#### get page HTML

    # makeJsonObj(pageLists)
    # getPageContents(driver, adListJson)

    pageContent = []
    adObj = json.loads(adListJson)

    for indexB, itemB in enumerate(adObj):
        driver.get(itemB["link"])
        adTable = driver.find_element_by_id("Onlnad")
        adContTable = adTable.get_attribute("innerHTML")
        itemB["content"] = adContTable
        adTitle = itemB["title"].encode('utf-8').strip()
        adLink = itemB["link"].encode('utf-8').strip()
        adContent = itemB["content"].encode('utf-8').strip()
        # from IPython import embed; embed()
        with connection.cursor() as cursor:
            sql = "INSERT INTO `frysad` (`title`, `link`, `content`, `dateadded`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (adTitle, adLink, adContent, '12345'))
            connection.commit()

        # mainAdList.append(itemB)
        # mainAdList[indexB] = itemB

    #### MySQL Info
    connection.close()

    # from IPython import embed; embed()
    # text_file = open("outfile.txt", "w")
    # text_file.write(str(mainAdList))
    # text_file.close()

if __name__ == "__main__":
    driver = init_driver()
    getIndex(driver)
    time.sleep(5)
    driver.quit()