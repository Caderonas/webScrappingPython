import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from bs4 import BeautifulSoup

""" Webscrapping of The pirate bay 
    and 1337 website, to get the list 
    of 10 best seeds in class torrent
    You can get the list as return 
    with the get_result function

"""

class WebScrapping:
    def __init__(self, search_keyword):
        driver = self.configure_firefox_driver()
        self.resultWS = self.getPirateBay(driver, search_keyword)
        self.resultWS += self.get1337(driver, search_keyword)
        self.resultWS.sort(key=lambda x: x.seed, reverse=True)
        driver.close()

    def configure_firefox_driver(self):
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--ignore-certificate-errors")
        firefox_options.add_argument("--incognito")
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path = "geckodriver", options = firefox_options)
        return driver

    def get_result(self):
        return self.resultWS 
    class Torrent:
        def __init__(self, name, date, size, seed, leech, link):
            self.name = name
            self.date = date
            self.size = float(size)
            self.seed = int(seed)
            self.leech= int(leech)
            self.link = link
        
        def setLink(self, link):
            self.link = link

    def uniSize(self, string):
        string = string.lower()
        coef = 0
        numb = float(re.search('[+-]?([0-9]*[.])?[0-9]+', string).group(0))
        if string.find('k') != -1:
            coef = 2
        elif string.find('m') != -1:
            coef = 1
        return round(numb/(1024**coef), 3)    

    def getPirateBay(self, driver, search_keyword):
        list_torrents = []
        driver.get(f"https://thepiratebay.org/search.php?q="+search_keyword+"&all=on&search=Pirate+Search&page=0&orderby=")
        WebDriverWait(driver, 5).until(
            lambda s: s.find_element(By.ID,"torrents").is_displayed()
        )
        soup = BeautifulSoup(driver.page_source, "lxml")
        for torrents in soup.select("ol.view-single"):
            for torrent in torrents.select("li.list-entry"):
                list_torrents.append(self.Torrent(  torrent.select_one("span.item-name").text,
                                                    torrent.select_one("span.item-uploaded").text,
                                                    self.uniSize(torrent.select_one("span.item-size").text),
                                                    torrent.select_one("span.item-seed").text,
                                                    torrent.select_one("span.item-leech").text,
                                                    torrent.select("span.item-name > a")[0]["href"]))
        list_torrents.sort(key=lambda x: x.seed, reverse=True)
        list_torrents = list_torrents[0:9]
        for torrent in list_torrents:
            driver.get(f"https://thepiratebay.org"+torrent.link)
            soup = BeautifulSoup(driver.page_source, "lxml")
            torrent.setLink(soup.select("a")[10]["href"]) #Set to one but 2
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
                list_torrents.append(self.Torrent(  torrent.select("td.coll-1 > a")[1].text,
                                                    torrent.select_one("td.coll-date").text,
                                                    self.uniSize(torrent.select_one("td.coll-4").text),
                                                    torrent.select_one("td.coll-2").text,
                                                    torrent.select_one("td.coll-3").text,
                                                    torrent.select("td.coll-1 > a")[1]["href"]))
        list_torrents.sort(key=lambda x: x.seed, reverse=True)
        list_torrents = list_torrents[0:9]
        for torrent in list_torrents:
            driver.get(f"https://1337x.to"+torrent.link)
            soup = BeautifulSoup(driver.page_source, "lxml")
            torrent.setLink(soup.select("div.clearfix")[2].select_one("a")["href"])
        return list_torrents

list_scrap = WebScrapping("lord of the rings").get_result()
for torrent in list_scrap:
    print({
        "Name : "+ torrent.name,
        "Seed : "+ str(torrent.seed)
    })