from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv,time

class fitgirlRepack():
    def __init__(self) -> None:
        pass
    
    def header(self):
        header = ['Game Title','Release Date','Genres Tags','Companies','Language','Comments','Orignal Size','Repack Size','Game Url','Download Link','Images','Features']
        
        with open(file="fitGirlRepack.csv",mode='w',newline='') as file:
            csv.writer(file).writerow(header)
    
    def userSearch(self):
        inputSearch = input('enter search about your game:- ')
        querry = '+'.join(inputSearch.split())
        return querry

    def openBrowser(self):
        driverPath = ChromeDriverManager().install()
        servc = Service(driverPath)
        driver = webdriver.Chrome(service=servc)
        return driver
    
    def getAndSaveLinks(self,driver):
        urlTag = driver.find_elements(By.XPATH,'//article//h1/a')
        for tag in urlTag:
            productLinks = tag.get_attribute('href')
            with open(file='productLinks.txt',mode='a') as file:
                file.write(productLinks + '\n')
    
    def readData(self):
        with open(file='productLinks.txt',mode='r') as file:
            readData = file.readlines()
            productUrls = [data.strip() for data in readData]
            return productUrls
    
    def parseData(self,driver,productUrls):
        for url in productUrls:
            driver.get(url)
            time.sleep(4)    
            try: title = driver.find_element(By.XPATH,'//article//h1').text.strip()
            except: title = 'None'
            try: releaseDate = driver.find_element(By.XPATH,'//span/a/time').text.strip()
            except: releaseDate = 'None'
            try: comments = driver.find_element(By.XPATH,'//span[@class="comments-link"]/a').get_attribute('textContent').strip()
            except: comments = 'None'
            try: genresTags = driver.find_element(By.XPATH,'//div[@class="entry-content"]/p[1]/strong[1]').text.strip()
            except: genresTags = 'None'
            try: companies = driver.find_element(By.XPATH,'//div[@class="entry-content"]/p[1]/strong[2]').text.strip()
            except: companies = 'None'
            try: language = driver.find_element(By.XPATH,'//div[@class="entry-content"]/p[1]/strong[3]').text.strip()
            except: language = 'None'
            try: orignalSize = driver.find_element(By.XPATH,'//div[@class="entry-content"]/p[1]/strong[4]').text.strip()
            except: orignalSize = 'None'
            try: repackSize = driver.find_element(By.XPATH,'//div[@class="entry-content"]/p[1]/strong[5]').text.strip()
            except: repackSize = 'None'
            try: downloadLink = driver.find_element(By.XPATH,'//div[@class="entry-content"]/ul/li/a').get_attribute('href')
            except: downloadLink = 'None'
            try:
                imagesTag = driver.find_elements(By.XPATH,'//div[@class="entry-content"]/p/a/img')
                images = '\n'.join([tag.get_attribute('src') for tag in imagesTag])
            except: images = 'None'
            try: features = driver.find_element(By.XPATH,'//div[@class="entry-content"]/ul[2]').get_attribute('innerText')
            except: features = 'None'
            row = [title,releaseDate,genresTags,companies,language,comments,orignalSize,repackSize,url,downloadLink,images,features]
            print(f"[Info] Getting Product:- {title}")
            self.saveData(row)
    
    def saveData(self,row):
        with open(file="fitGirlRepack.csv",mode='a',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(row)

    def run(self):
        domain = 'https://fitgirl-repacks.site/?s='
        querry = self.userSearch()
        webUrl = f"{domain}{querry}"
        print(f"\n[Info] Getting data from Url:- {webUrl}\n")
        driver = self.openBrowser()
        driver.get(webUrl)
        while True:
            time.sleep(4)
            try:
                nextPage = driver.find_element(By.XPATH,'//a[@class="next page-numbers"]')
                if nextPage:
                    nextPage.click()
                    self.getAndSaveLinks(driver)
            except: break
        productUrls = self.readData()
        self.parseData(driver,productUrls)

open(file='productLinks.txt',mode='w').close()
myClass = fitgirlRepack()
print(f"[Info] Do you want to delete all data and add new data! ")
answer = input('enter your decision (y/n):- ')
if answer == 'y':
    myClass.header()
    myClass.run()
else:
    myClass.run()

