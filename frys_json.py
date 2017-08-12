import datetime, time
import pymysql.cursors
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

today = datetime.date.strftime(datetime.date.today(), "%m%d%y")

def init_driver():
    # driver = webdriver.Firefox()
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.wait = WebDriverWait(driver, 5)
    return driver

def getIndex(driver, driver2):

    idn = 001
    pageLists = []
    adList = []
    mainAdList = []
    adElem = {}
    pageContent = []

    frysAdData = { "name":"Fry's Weekly Ad","dateScraped":today,"pages":[]}

    driver.get("http://www.frys.com/ads/view-all-store-ads")
    parentElement = driver.find_element_by_class_name("items")
    elementList = parentElement.find_elements_by_class_name("thumbnail_set")

    for index,item in enumerate(elementList):
        pages = elementList[index].find_elements_by_tag_name("a")
        for index,item in enumerate(pages):
            pageLists.append(item)

            innerElem = item.find_elements_by_tag_name("img")
            adTitle = innerElem[0].get_attribute("alt").encode('utf-8').replace('Frys Ad ','')
            adThumb = innerElem[0].get_attribute("src")
            adLink = item.get_attribute("href").encode('utf-8').strip()

            driver2.get(adLink)
            adContent = driver2.find_element_by_id("Onlnad").get_attribute("innerHTML").encode('utf-8').strip()

            frysAdData["pages"][adTitle]
            frysAdData["pages"][adTitle]["link"] = adLink
            frysAdData["pages"][adTitle]["thumbnail"] = adThumb
            frysAdData["pages"][adTitle]["content"] = adContent.replace('"','\"')

            from IPython import embed; embed()

if __name__ == "__main__":
    driver = init_driver()
    driver2 = init_driver()
    getIndex(driver, driver2)
    time.sleep(5)
    driver.quit()