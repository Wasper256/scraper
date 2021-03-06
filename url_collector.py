"""Part, that collecting, writting and setting URLs."""
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import main
import time


def url():
    """Collecting product URLs and writting into file."""
    with main.ControlledExecution() as driver:
        driver.set_page_load_timeout(60)
        url_iter = 1
        with open("links.txt", 'w') as file:
            while url_iter < 14:
                # loading page
                url = "https://search.jd.com/Search?keyword=qnap&enc=utf-8" + "&page=" + str(url_iter)
                driver.get(url)
                time.sleep(15)
                # driver.save_screenshot("1.png")
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
                            res_link = "https:" + l.get("href") + "\n"
                            file.write(res_link)
                url_iter = url_iter + 2
        driver.close
    return


def url_cleaner():
    """Rejecting URLs, that meet twice in file."""
    with open("links.txt", 'r') as file:
        urllist = file.read().splitlines()
        for x in urllist:
            ch = urllist.count(x)
            if ch > 1:
                urllist.remove(x)
    return(urllist)
