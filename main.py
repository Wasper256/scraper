# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import unicodecsv

driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
driver.set_page_load_timeout(300)


def main():
    # url_collector()
    with open("links.txt", 'r') as file:
        urllist = file.read().splitlines()
    for x in urllist:
        ch = urllist.count(x)
        if ch > 1:
            urllist.remove(x)
    # with open('output.csv', 'w') as csvfile:
    #    fieldnames = ['Brand', 'MPN', 'URL', 'Name', 'Price', 'Stock']
    #    writer = unicodecsv.DictWriter(csvfile, fieldnames=fieldnames)
    #    writer.writeheader()
    #    for y in urllist:
    scraper()


def url_collector():
    url_iter = 1
    print("Processing page 1 for item URLs...")
    while url_iter < 14:
        try:
            url = "https://search.jd.com/Search?keyword=qnap&enc=utf-8&page=" + str(url_iter)
            driver.get(url)
            try:
                driver.find_element_by_xpath('//*[@id="J_scroll_loading"]').click()
            except:
                pass
            try:
                WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.ID, "J_scroll_loading")))
            finally:
                pass
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
            print("Processing page " + str((url_iter + 1) / 2) + " for item URLs...")
        except:
            pass
    print("done")


def scraper():
    URL = "http://item.jd.com/10346678743.html"
    MPN = URL.replace(".html", '').replace("http://item.jd.com/", '')
    driver.get(URL)
    try:
        driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[2]').click()
    finally:
        pass
    try:
        WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.ID, "J-detail-content")))
    finally:
        pass
    try:
        driver.find_element_by_xpath('//*[@id="detail"]/div[1]/ul/li[1]').click()
    finally:
        pass
    soup = BeautifulSoup(driver.page_source, "html.parser")
    g_data = soup.find_all("div", {"class": "itemInfo-wrap"})
    for item in g_data:
        Name = (item.find_all("div", {"class": "sku-name"})[0].text)
        Price = (item.find_all("span", {"class": "p-price"})[0].text)
        for a in item.find_all("a", {"id": "InitCartUrl"}):
            st = a['href']
            if st == '#none':
                Stock = 0
            else:
                Stock = 1
    m_data = soup.find_all("div", {"class": "p-parameter"})
    for item in m_data:
        Brand = (item.find_all("a")[0].text)
        Brand = Brand.decode('gb2312').encode('utf-8')
    print Brand + MPN + URL + Name + Price
    with open('output.csv', 'wb') as csvfile:
        w = unicodecsv.writer(csvfile, encoding='utf-8-sig')
        print Brand.encode('utf-8')
        op = {'Brand': str(Brand).encode('utf-8'), 'MPN': str(MPN), 'URL': str(URL), 'Name': str(Name).encode('utf-8'), 'Price': str(Price), 'Stock': str(Stock)}
        print op()
        w.writerow(op)


if __name__ == '__main__':
    main()
driver.close()
