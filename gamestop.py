import csv,time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class gameStop():
    def __init__(self) -> None:
        pass

    def header(self):
        header = ['Game Title','Game Url','Image','Publisher Name','Ratting Average','Ratting','Availbilty','Price','Bread Crumbs','Description']
        with open(file='GameStop.csv',mode='w',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(header)

    def openBrowser(self):
        driverPath = ChromeDriverManager().install()
        servc = Service(driverPath)
        browser = webdriver.Chrome(service=servc)
 
    
    def getproductLinks(self,browser,weburl):
        browser.get(weburl)
        time.sleep(4)
        productLinkTag = browser.find_elements(By.XPATH,'//div[@data-list-item-type="Product list"]//a[@class="product-tile-link"]')
        for tag in productLinkTag:
            productLink = tag.get_attribute('href')
            with open(file='productinks.txt',mode='a') as file:
                file.write(productLink+'\n')
    
    def readDatafromTxt(self):
        with open(file='productinks.txt',mode='r') as file:
            readData = file.readlines()
            productLinks = [link.strip() for link in readData]
         
    
    def parseData(self,browser,productLinks):
        for url in productLinks:
            browser.get(url)
            time.sleep(4)
            try: title = browser.find_element(By.XPATH,'//h2[contains(@class,"product-name")]').text.strip()
            except: title = 'None'
            try: price = browser.find_element(By.XPATH,'//div[@class="price-update"]//span[contains(@class,"actual-price actual-price")]').get_attribute('innerText')
            except: price = 'None'
            try: rattingAverage = browser.find_element(By.XPATH,'//div[@class="review-count"]').get_attribute('innerText')
            except: rattingAverage = 'None'
            try: ratting = browser.find_element(By.XPATH,'//div[contains(@class,"reviewHeader")]/h1[@class="rating-value"]').text.strip()
            except: ratting = 'None'
            try: image = browser.find_element(By.XPATH,'//div[@class="product-main-image-gallery"]/picture/img').get_attribute('src')
            except: image = 'None'
            try:
                availbiltyTag = browser.find_element(By.XPATH,'//div[@id="primary-details"]//button[@id="add-to-cart"]')
                availbilty = 'In Stock' if availbiltyTag.text == 'Add to Cart' else 'None'
            except: availbilty = 'None'
            try: description = browser.find_element(By.XPATH,'//div[@class="short-description"]').text.strip() 
            except: availbilty = 'None'
            try: 
                breadCrumbsTag = browser.find_elements(By.XPATH,'//ol[@class="breadcrumb"]')
                cleartag = ''.join(['Home\n']+[tag.text.strip() for tag in breadCrumbsTag])
                breadCrumbs = ' > '.join(cleartag.split('\n'))
            except: breadCrumbs = 'None'
            try: publisherName = browser.find_element(By.XPATH,'//span[@class="product-publisher"]').get_attribute('innerText').strip()
            except: publisherName = 'None'
            row = [title,url,image,publisherName,rattingAverage,ratting,availbilty,price,breadCrumbs,description]
            self.saveData(row)
            print(f"[Info] Getting Product:- {title}")
        
    def saveData(self,row):
        with open(file='GameStop.csv',mode='a',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(row)
    
    def run(self):
        weburl = 'https://www.gamestop.com/video-games/playstation-4'
        browser = self.openBrowser()
        self.getproductLinks(browser,weburl)
        productUrls = self.readDatafromTxt()
        self.parseData(browser,productUrls)


open(file='productinks.txt',mode='w').close()
myClass = gameStop()
print(f"[Info] Do you want to delete all data and add new data! ")
answer = input('enter your decision (y/n):- ')
if answer == 'y':
    myClass.header()
    myClass.run()
else:
    myClass.run()
