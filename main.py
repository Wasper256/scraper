# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


driver = webdriver.PhantomJS()
driver.set_page_load_timeout(60)


def main():
    # url_collector()
    with open("links.txt", 'r') as file:
        urllist = file.read().splitlines()
        print(len(urllist))
    for x in urllist:
        ch = urllist.count(x)
        if ch > 1:
            urllist.remove(x)
    print(len(urllist))
    for y in urllist:
        scraper(y)


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
                        res_link = "https:" + l.get("href") + "\n"
                        with open("links.txt", 'a') as file:
                            file.write(res_link)
            url_iter = url_iter + 2
            print("Processing page " + str((url_iter + 1) / 2) + " for item URLs...")
        except:
            pass
    print("done")


def scraper(y):
    url = y
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    g_data = soup.find_all("div", {"class": "goods-list-v2 gl-type-1 J-goods-list"})
    for item in g_data:
        obj = (item.contents[0].find_all("div", {"class": "p-name p-name-type-2"}))


if __name__ == '__main__':
    main()
driver.close()
