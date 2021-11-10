from stem import Signal
from stem.control import Controller
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager 
from bs4 import BeautifulSoup

# signal TOR for a new connection
def switchIP():
    with Controller.from_port(port = 4444) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

# get a new selenium webdriver with tor as the proxy
def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    browser = webdriver.Firefox(executable_path=”/home/linuxbrew/.linuxbrew/Cellar/geckodriver/0.30.0/bon/geckodriver”)
    
    
    return driver
proxy = my_proxy("127.0.0.1", 9050)
proxy.get("http://piratebayo3klnzokct3wt5yyxb2vpebbuyjl7m623iaxmqhsd52coid.onion")
html = proxy.page_source
soup = BeautifulSoup(html, 'lxml')
print(soup)
switchIP()
"""
def create_torbrowser_webdriver_instance():
    DRIVER_PATH = './drivers/geckodriver'
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")

    driver = webdriver.Firefox(options=options, executable_path=DRIVER_PATH)
    driver.get("https://www.nintendo.com/")
    print(driver.page_source)
    driver.quit()

if __name__ == '__main__':
    create_torbrowser_webdriver_instance()

def searchEngine(name):
    name = name.replace(" ", "+")
    source = requests.get('https://thepiratebay.org/search.php?q='+name+'&all=on&search=Pirate+Search&page=0&orderby=').text
    print ('https://thepiratebay.org/search.php?q='+name+'&all=on&search=Pirate+Search&page=0&orderby=')

    soup = BeautifulSoup(source, 'lxml')
    print (soup.prettify())

searchEngine("lord of the ring")
"""