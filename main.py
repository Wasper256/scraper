# -*- coding: utf-8 -*-
from selenium import webdriver
import unicodecsv
import url_collector
import scrap


def main():
    url_collector.url()
    urllist = url_collector.url_cleaner()
    # creating .csv file
    with open('output.csv', 'wb') as csvfile:
        fieldnames = ["Brand", "MPN", "URL", "Name", "Price", "Stock"]
        unicodecsv.DictWriter(csvfile, fieldnames=fieldnames).writeheader()
        # scraping URLs
        for y in urllist:
            op = scrap.scraper(y)
            w = unicodecsv.DictWriter(csvfile, encoding='utf-8-sig', fieldnames=fieldnames)
            w.writerow(op)


class ControlledExecution:
    def __enter__(self):
        return webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])

    def __exit__(self, type, value, traceback):
        return isinstance(value, TypeError)


if __name__ == '__main__':
        main()
