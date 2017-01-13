# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def main():
    url_itr = 1
    with open("links.txt", 'a') as file:

        url = "https://search.jd.com/Search?keyword=qnap&enc=utf-8&page={0}".format(url_itr)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        g_data = soup.find_all("div", {"class": "goods-list-v2 gl-type-1 J-goods-list"})
        for item in g_data:
            obj = (item.contents[0].find_all("div", {"class": "p-name p-name-type-2"}))
            for link in obj:
                rl = link.find_all("a")
                for l in rl:
                    res_link = "https:" + l.get("href") + "\n"
                    print res_link
                    file.write(res_link)

if __name__ == '__main__':
    main()
