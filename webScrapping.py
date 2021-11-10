import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup

class WebScrapping:
    resultWS = []
    def __init__(self, search_keyword):
        driver = self.configure_firefox_driver()
        self.resultWS += self.getPirateBay(driver, search_keyword)
        self.resultWS += self.get1337(driver, search_keyword)
        driver.close()

    class Torrent:
        def __init__(self, name, date, size, seed, leech):
            self.name = name
            self.date = date
            self.size = float(size)
            self.seed = int(seed)
            self.leech= int(leech)

    def configure_firefox_driver(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--ignore-certificate-errors")
        firefox_options.add_argument("--incognito")
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path = "geckodriver", options = firefox_options)
        return driver

    def getPirateBay(self, driver, search_keyword):
        list_torrents = []
        driver.get(f"https://thepiratebay.org/search.php?q="+search_keyword+"&all=on&search=Pirate+Search&page=0&orderby=")
        WebDriverWait(driver, 5).until(
            lambda s: s.find_element(By.ID,"torrents").is_displayed()
        )
        soup = BeautifulSoup(driver.page_source, "lxml")
        for torrents in soup.select("ol.view-single"):
            for torrent in torrents.select("li.list-entry"):
                torrent_name = "span.item-name"
                torrent_date = "span.item-uploaded"
                torrent_size = "span.item-size"
                torrent_seed = "span.item-seed"
                torrent_leech= "span.item-leech"
                list_torrents.append(self.Torrent( torrent.select_one(torrent_name).text,
                                                torrent.select_one(torrent_date).text,
                                                self.uniSize(torrent.select_one(torrent_size).text),
                                                torrent.select_one(torrent_seed).text,
                                                torrent.select_one(torrent_leech).text))
        return list_torrents

    def get1337(self, driver, search_keyword):
        list_torrents = []
        driver.get(f"https://1337x.to/search/"+search_keyword+"/1/")
        WebDriverWait(driver, 5).until(
            lambda s: s.find_element(By.CLASS_NAME,"table-list").is_displayed()
        )
        soup = BeautifulSoup(driver.page_source, "lxml")
        for torrents in soup.select("table.table-list > tbody"):
            for torrent in torrents.select("tr"):
                torrent_name = "td.coll-1 > a"
                torrent_date = "td.coll-date"
                torrent_size = "td.coll-4"
                torrent_seed = "td.coll-2"
                torrent_leech= "td.coll-3"

                list_torrents.append(self.Torrent(   torrent.select(torrent_name)[1].text,
                                                torrent.select_one(torrent_date).text,
                                                self.uniSize(torrent.select_one(torrent_size).text),
                                                torrent.select_one(torrent_seed).text,
                                                torrent.select_one(torrent_leech).text))
        return list_torrents



    def uniSize(self, string):
        string = string.lower()
        coef = 0
        numb = float(re.search('[+-]?([0-9]*[.])?[0-9]+', string).group(0))
        if string.find('k') != -1:
            coef = 2
        elif string.find('m') != -1:
            coef = 1
        return round(numb/(1024**coef), 3)

def main():
    search_keyword = "lord of the ring"
    list_pirate = WebScrapping(search_keyword).resultWS
    for torrent in list_pirate:
        print ("")
        print(torrent.size)

main()