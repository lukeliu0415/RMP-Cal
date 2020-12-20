from selenium import webdriver
from bs4 import BeautifulSoup

def parse(url):
    driver = webdriver.Chrome(executable_path="/users/lukeliu/chromedriver")
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    result = soup.find(class_ = "filter-sidebar")
    return result

print(parse('https://www.berkeleytime.com/catalog/compsci/70/'))
