# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import unicodecsv

driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
driver.set_page_load_timeout(30)


def main():
    url_collector()
    with open("links.txt", 'r') as file:
        urllist = file.read().splitlines()
    # rejecting URLs, that meet twice in file
    for x in urllist:
        ch = urllist.count(x)
        if ch > 1:
            urllist.remove(x)
    # creating .csv file
    with open('output.csv', 'wb') as csvfile:
        fieldnames = ["Brand", "MPN", "URL", "Name", "Price", "Stock"]
        unicodecsv.DictWriter(csvfile, fieldnames=fieldnames).writeheader()
    # scraping URLs
    for y in urllist:
        scraper(y, fieldnames)


def url_collector():
    url_iter = 1
    while url_iter < 14:
        try:
            # loading page
            url = "https://search.jd.com/Search?keyword=qnap&enc=utf-8" + "&page=" + str(url_iter)
            driver.get(url)
            # activating JavaScript, that loads second part of page
            try:
                driver.find_element_by_xpath('//*[@id="J_scroll_loading"]').click()
            except:
                pass
            try:
                WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.ID, "J_scroll_loading")))
            finally:
                pass
            # collecting URLs
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            g_data = soup.find_all("div", {"class": "goods-list-v2 gl-type-1 J-goods-list"})
            for item in g_data:
                obj = (item.contents[0].find_all("div", {"class": "p-name p-name-type-2"}))
                for link in obj:
                    rl = link.find_all("a")
                    for l in rl:
                        res_link = "http:" + l.get("href") + "\n"
                        with open("links.txt", 'a') as file:
                            file.write(res_link)
            url_iter = url_iter + 2
        except:
            pass


def scraper(y, fieldnames):
    try:
        url = y
        # collecting MPN from URL
        mpn = url.replace(".html", '').replace("http://item.jd.com/", '')
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
        with open('output.csv', 'ab') as csvfile:
            w = unicodecsv.DictWriter(csvfile, encoding='utf-8-sig', fieldnames=fieldnames)
            op = {"Brand": brand, "MPN": mpn, "URL": url, "Name": name, "Price": price, "Stock": stock}
            w.writerow(op)
    except:
        return


if __name__ == '__main__':
    main()
driver.close()
