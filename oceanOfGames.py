from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time,csv

class oceanOFGames():
    def __init__(self) -> None:
        pass
    
    def header(self):
        header = ['Games Title','Games Url','Image','Specifications','Minium Requires','Recommended']
        with open(file='oceanOfGames.csv',mode='w',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(header)
    def yourSearch(self):
        inputSearch = input('enter your game search:- ')
        querry = '+'.join(inputSearch.split())
 
    
    def openBrowser(self):
        driverPath = ChromeDriverManager().install()
        servc = Service(driverPath)
        driver = webdriver.Chrome(service=servc)

    
    def getGamesLinks(self,driver,webUrl):
        driver.get(webUrl)
        allProductUrl = driver.find_elements(By.XPATH,'//div[@class="post-details"]/a')
        for link in allProductUrl:
            productLinks = link.get_attribute('href')
            with open(file='productLinks.txt',mode='a') as file:
                file.write(productLinks + '\n')
    
    def readData(self):
        with open(file='productLinks.txt',mode='r') as file:
            readData = file.readlines()
            productUrls = [lnk.strip() for lnk in readData]
   
    
    def parseData(self,driver,productUrls):
        for url in productUrls:
            driver.get(url)
            time.sleep(4)
            try: title = driver.find_element(By.XPATH,'//h1[@class="title"]').text.strip()
            except: 'None'
            try: image = driver.find_element(By.XPATH,'//div[@class="post-content clear-block"]/p[2]/img').get_attribute('src')
            except: image = 'None'
            try:
                specificationsTag = driver.find_elements(By.XPATH,'//div[@class="post-content clear-block"]/ul/li')
                specifications = [tag.text.strip() for tag in specificationsTag]
            except: specifications = 'None'
            try: 
                miniumRequiresTag = driver.find_elements(By.XPATH,'//p[contains(text(),"Requires ")][1]')
                miniumRequires = [x.text.strip().replace('*','') for x in miniumRequiresTag]
            except: miniumRequires = 'None'
            try: 
                recommendedTag = driver.find_elements(By.XPATH,'//p[contains(text(),"Requires ")][2]')
                recommended = [x.text.strip().replace('*','') for x in recommendedTag]
            except: recommended = 'None'
            row = [title,url,image,specifications,miniumRequires,recommended]
            print(f"[Info] Getting Game Data:- {title}")
            self.saveData(row)
    
    def saveData(self,row):
        with open(file='oceanOfGames.csv',mode='a',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(row)
    
    def run(self):
        driver = self.openBrowser()
        querry = self.yourSearch()
        for page in range(1,3):
            webUrl = f"https://oceansofgamess.com/page/{page}/?s={querry}"
            print(f"\n[Info] Getting data from Url:- {webUrl}\n")
            self.getGamesLinks(driver,webUrl)
            productLinks = self.readData()
            self.parseData(driver,productLinks)

open(file='productLinks.txt',mode='w').close()
myClass = oceanOFGames()
myClass.header()
myClass.run()
