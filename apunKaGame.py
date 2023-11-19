from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time,csv
import json

class ApunkaGame():
    def __init__(self) -> None:
        pass
    
    def header(self):
        header = ['Game Title','Image','Type Of Game','minimum Requries','Game Size','Password','How TO Download','How To Install']
        with open(file='ApunKaGames.csv',mode='w',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(header)
    
    def UserDemand(self):
        print(f"\n[INFO] What type of data do you want to scrape from  Catageories or User Search on this website")
        print(f"\n[Info] if do you want to scrape a Catageory Enter:- c")
        print(f"\n[Info] if do you want to scrape data with own search:- Enter s")
        Answer = input('enter your decision (c/s):- ')
        return Answer


    def openBrowser(self):
        driverpath = ChromeDriverManager().install()
        servc = Service(driverpath)
        driver = webdriver.Chrome(service=servc)
        return driver
    
    def userSearch(self):
        inputSearch = input('enter your game search:- ')
        cleanSearch = ''
        querry = f"https://www.apunkagames.biz/?s={cleanSearch}"
        print(f"\n[Info] Gettting data from this Url:- {querry}\n")
        return querry

    def getAndSaveLink(self,driver,querry):
        driver.get(querry)
        productTag = driver.find_elements(By.XPATH,'//article[contains(@class,"category-full-version-games")]/h2/a') or driver.find_elements(By.XPATH,'//table[@class="fixed"]/tbody/tr/td//a[1]')
        for tag in productTag:
            proUrls = tag.get_attribute('href')
            with open(file='ProductLinks.txt',mode='a') as file:
                file.write(proUrls+'\n')

    def readAndgetLink(self):
        with open(file='ProductLinks.txt',mode='r') as file:
            readData = file.readlines()
            productLinks = [data.strip() for data in readData]

    def selectSearch(self):
        with open(file='SaveCatageories.json', mode='r') as file:
            allResult = json.load(file)
        for index,data in enumerate(allResult):
            ResultName = f"{[index]}:- {data['CategoryName']}"
            print(ResultName)
        inputNumber = int(input('[INFO] enter your Index number in Catageories Names: '))
        NameTag = allResult[inputNumber]
        CatageoryTitle = NameTag['CategoryName']
        CatageoryUrl = allResult[inputNumber]['CategoryLinks']
        SelectedResult = f'\n\n{"You are selected this catageory for scrape Data ->"}{CatageoryTitle}'
        print(SelectedResult)
    
    def parseData(self,driver,productLinks):
        for url in productLinks:
            driver.get(url)
            time.sleep(4)
            try: title = driver.find_element(By.XPATH,'//h1[@class="page-title"]').text.strip()
            except: title = 'None'
            try: image = driver.find_element(By.XPATH,'//div[@itemprop="articleBody"]//a/img').get_attribute('src')
            except: image = 'None'
            try: 
                typeOfGameTag = driver.find_element(By.XPATH,'//div[@itemprop="articleBody"]//strong[contains(text(),"Release Date") ]/parent::span').text.strip()
                cleartag = typeOfGameTag.split('\n')
                typeOfGame = ''.join(cleartag[0])
            except: typeOfGame = 'None'
            try: minimumRequries = driver.find_element(By.XPATH,'//div[@itemprop="articleBody"]/ul').get_attribute('innerText')
            except: minimumRequries = 'None'
            try: howTODownload = driver.find_element(By.XPATH,'//b[text()="How to Download?"]/parent::div/a').get_attribute('href')
            except: howTODownload = 'None'
            try: howtoInstall = driver.find_element(By.XPATH,'//b[contains(text(), "How to Install?")]/parent::p/preceding-sibling::div/parent::div/ol').get_attribute('innerText')
            except: howtoInstall = 'None'
            try: 
                textTag = driver.find_element(By.XPATH,'//b[contains(text(),"Game Size:")]/parent::p').get_attribute('textContent')
                splittedTag = textTag.split('\n')
                gameSize = splittedTag[0]
                password = splittedTag[1]
            except: 
                gameSize = 'None'
                password = 'None'
            row = [title,image,typeOfGame,minimumRequries,gameSize,password,howTODownload,howtoInstall]
            print(f"[Info] Getting Games:- {title}")
            self.saveData(row)
    
    def saveData(self,row):
        with open(file='ApunKaGames.csv',mode='a',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(row)
    
    def run(self):
        driver = self.openBrowser()
        userAnswer = self.UserDemand()
        if userAnswer.lower() == 'c':
            catageoryUrl = self.selectSearch()
            self.getAndSaveLink(driver,catageoryUrl)
            productUrls = self.readAndgetLink()
            self.parseData(driver,productUrls)
        if userAnswer.lower() == 's':
            querry = self.userSearch()
            self.getAndSaveLink(driver,querry)
            productLinks = self.readAndgetLink()
            self.parseData(driver,productLinks)

open(file='ProductLinks.txt',mode='w').close()
myClass = ApunkaGame()
print(f"[Info] Do you want to delete all data and add new data! ")
answer = input('enter your decision (y/n):- ')
if answer == 'y':
    myClass.header()
    myClass.run()
else:
    myClass.run()