import re
import sys
import subprocess
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

""" Webscrapping of The pirate bay 
    and 1337 website, to get the list 
    of 10 best seeds in class torrent
    You can get the list as return 
    with the get_result function

"""
def configure_firefox_driver():
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--ignore-certificate-errors")
    firefox_options.add_argument("--incognito")
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(executable_path = GeckoDriverManager().install(), options = firefox_options)
    return driver
class WebScrapping:

    def __init__(self, search_keyword):
        #start = time.time()
        """ Driver """
        #self.state = "Starting driver..."
        driver = configure_firefox_driver()
        #self.state = "Driver charged : "+ str(time.time() - start)
        self.resultWS = []
        while True:
            try:
                #start = time.time()
                #self.state = "PirateBay ..."
                self.resultWS += self.getPirateBay(driver, search_keyword)
                #self.state = "PirateBay charged " + str(time.time() - start)
                break
            except IndexError:
                print ("PirateBay : Dammn shit, a page didn't charge well")
            except AttributeError:
                print ("PirateBays : Connect the VPN")
        while True:
            try:
                #start = time.time()
                #self.state = "1337 ..."
                self.resultWS += self.get1337(driver, search_keyword)
                #self.state = "1337 charged " + str(time.time() - start)
                break
            except IndexError:
                print ("1337 : Dammn shit, a page didn't charge well")
            except AttributeError:
                print ("1337 : Connect the VPN")
        
        self.resultWS.sort(key=lambda x: x.seed, reverse=True)
        driver.close()

    

    def get_result(self):
        """
        os.chdir(r"./webScrappingPython/")
        print (os.getcwd())
        with open(r"./torrents.json", "r+") as file:
            file_data = json.load(file)
            for torrent in self.resultWS:
                jsonStr = json.dumps(torrent)
                file_data.append(jsonStr)
            json.dump(self.resultWS, file, indent=4)
        file.close()
        """
        return self.resultWS

    class Torrent:
        def __init__(self, src, name, date, size, seed, leech, link):
            self.src = src
            self.name = name
            self.date = date
            self.size = float(size)
            self.seed = int(seed)
            self.leech= int(leech)
            self.link = link
        
        def set_link(self, link):
            self.link = link
        #@Slot()
        def get_magnet(self):
            driver = configure_firefox_driver()
            driver.get(self.link)
            soup = BeautifulSoup(driver.page_source, "lxml")
            if self.src == "PirateBay":
                magnet = soup.select("a")[10]["href"]
            elif self.src == "1337":
                magnet = soup.select("div.clearfix")[2].select_one("a")["href"]
            driver.close()
            subprocess.call("peerflix "+ magnet + " --vlc")
    """
    def get_stream(self, id):
        self.magnet = self.resultWS[id].get_magnet()
        return self.magnet
    """
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
        """
        WebDriverWait(driver, 5).until(
            lambda s: s.find_element(By.ID,"torrents").is_displayed()
        )
        """
        soup = BeautifulSoup(driver.page_source, "lxml")
        for torrents in soup.select("ol.view-single"):
            for torrent in torrents.select("li.list-entry"):
                list_torrents.append(self.Torrent(  "PirateBay",
                                                    torrent.select_one("span.item-name").text,
                                                    torrent.select_one("span.item-uploaded").text,
                                                    self.uniSize(torrent.select_one("span.item-size").text),
                                                    torrent.select_one("span.item-seed").text,
                                                    torrent.select_one("span.item-leech").text,
                                                    "https://thepiratebay.org"+torrent.select("span.item-name > a")[0]["href"]))
                if len(list_torrents) == 10:
                    return list_torrents
        """
        list_torrents.sort(key=lambda x: x.seed, reverse=True)
        list_torrents = list_torrents[0:9]
        
        for torrent in list_torrents:
            driver.get(f"https://thepiratebay.org"+torrent.link)
            soup = BeautifulSoup(driver.page_source, "lxml")
            torrent.set_link(soup.select("a")[10]["href"]) 
        """
        return list_torrents

    def get1337(self, driver, search_keyword):
        list_torrents = []
        driver.get(f"https://1337x.to/search/"+search_keyword+"/1/")
        """
        WebDriverWait(driver, 5).until(
            lambda s: s.find_element(By.CLASS_NAME,"table-list").is_displayed()
        )
        """
        soup = BeautifulSoup(driver.page_source, "lxml")
        for torrents in soup.select("table.table-list > tbody"):
            for torrent in torrents.select("tr"):
                list_torrents.append(self.Torrent(  "1337",
                                                    torrent.select("td.coll-1 > a")[1].text,
                                                    torrent.select_one("td.coll-date").text,
                                                    self.uniSize(torrent.select_one("td.coll-4").text),
                                                    torrent.select_one("td.coll-2").text,
                                                    torrent.select_one("td.coll-3").text,
                                                    "https://1337x.to"+torrent.select("td.coll-1 > a")[1]["href"]))
                if len(list_torrents) == 10:
                    return list_torrents
        """
        list_torrents.sort(key=lambda x: x.seed, reverse=True)
        list_torrents = list_torrents[0:9]
        
        for torrent in list_torrents:
            driver.get(f"https://1337x.to"+torrent.link)
            soup = BeautifulSoup(driver.page_source, "lxml")
            torrent.set_link(soup.select("div.clearfix")[2].select_one("a")["href"])
        """
        return list_torrents

'''
if __name__ == "__main__":
    # Qt Application
    start = time.time()
    torrents = WebScrapping("lord of the ring").get_result()
    
    print (time.time()-start)
    for torrent in torrents:
        print (torrent.name)
'''