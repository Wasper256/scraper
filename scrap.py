
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import main


def scraper(y):
    soup = loader(y)
    op = collector(soup, y)
    return op


def loader(url):
    with main.ControlledExecution() as driver:
        # Loading page. Page is heavy that is why here i trying load page 3 times.
        try:
            driver.set_page_load_timeout(30)
            driver.get(url)
        except:
            try:
                driver.set_page_load_timeout(60)
                driver.get(url)
            except:
                try:
                    driver.set_page_load_timeout(120)
                    driver.get(url)
                except:
                    return()
        # extracting price and product availability, that loaded by JavaScript
        try:
            driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[3]').click()
        except:
            try:
                driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[2]').click()
            except:
                driver.find_element_by_xpath('//*[@id="detail-tab-param"]').click()
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.ID, "J-detail-content")))
        try:
            driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[1]').click()
        except:
            driver.find_element_by_xpath('//*[@id="detail-tab-intro"]').click()
        # collecting data
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        return soup


def collector(soup, url):
    # collecting MPN from URL
    mpn = url.replace(".html", '').replace("http://item.jd.com/", '')
    g_data = soup.find_all("div", {"class": "itemInfo-wrap"})
    if not g_data:
        g_data = soup.find_all("div", {"id": "itemInfo"})
    for item in g_data:
        # collecting product name
        if (item.find_all("div", {"class": "sku-name"})):
            name = (item.find_all("div", {"class": "sku-name"})[0].text)
        else:
            name = (item.find_all("div", {"id": "name"})[0].text)
        # collecting price
        if (item.find_all("span", {"class": "p-price"})):
            price = (item.find_all("span", {"class": "p-price"})[0].text)
        else:
            price = (item.find_all("strong", {"class": "p-price"})[0].text)
        # cheking "in Stock?"
        for a in item.find_all("a", {"id": "InitCartUrl"}):
            st = a['href']
            if st == '#none':
                stock = 0
            else:
                stock = 1
    m_data = soup.find_all("div", {"class": "p-parameter"})
    # collecting product brand
    for item in m_data:
        brand = (item.find_all("a")[0].text)
    # writing collected data into .csv file
    op = {"Brand": brand, "MPN": mpn, "URL": url, "Name": name, "Price": price, "Stock": stock}
    return op
