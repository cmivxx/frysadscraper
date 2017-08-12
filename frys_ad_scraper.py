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
    # Connect to the database
    connection = pymysql.connect(host='api.cmivxx.com',
                                 user='frysad',
                                 password='*password_here*',
                                 db='cm_homep',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    idn = 001
    pageLists = []
    adList = []
    mainAdList = []
    adElem = {}
    pageContent = []

    try:
        with connection.cursor() as rmcursor:
            sql_del = "DELETE FROM frysad"
            rmcursor.execute(sql_del)
            rmcursor.close()
            connection.commit()
            print("Cleared DB; Starting fresh.")
    except:
        print("Error: DB Cleaning Failed")

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

            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `frysad` (`idnum`, `title`, `link`, `thumb`, `content`, `dateadded`) VALUES (%s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (idn, adTitle, adLink, adThumb, adContent, today))
                    cursor.close()
                    connection.commit()
                    print(adTitle)
                    idn += 1
            except:
                print("Something broke while trying to add the item to the DB.  Skipping this item.")

    connection.close()


if __name__ == "__main__":
    driver = init_driver()
    driver2 = init_driver()
    getIndex(driver, driver2)
    time.sleep(5)
    driver.quit()