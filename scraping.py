from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import csv
import sqlite3
import sys
from datetime import datetime
database = sqlite3.connect("articles.db")
class automate(webdriver.Chrome,By,NoSuchElementException):
    def __init__(self):
        super().__init__()
        self.maximize_window()
        self.get("https://www.theverge.com/")
    def  getdetails(self):
        date = datetime.today()
        filename = f'{date.day}{date.month}{date.year}_verge.csv'
        try:
            readlines = csv.reader(open(filename,'r'))
            id = len(list(readlines))-1
            csvwriter = csv.DictWriter(open(filename,'a',newline=''),fieldnames=['id','URL','headline','Author','date'])
        except FileNotFoundError:
            csvwriter = csv.DictWriter(open(filename,'a',newline=''),fieldnames=['id','URL','headline','Author','date'])
            csvwriter.writeheader()
            id=0
                       
        oldtitle = " "
        while True:
            try:
                date = self.find_element(self.CLASS_NAME,"duet--article--timestamp")
                author = self.find_elements(self.CLASS_NAME, "tracking-6")
                title = self.find_element(self.CSS_SELECTOR,".inline.font-polysans.text-22.font-bold.leading-110")
                if title is not None and oldtitle != title and author is not None and date is not None:
                    print(f'inside {id}')
                    date = self.date(date.text)
                    csvwriter.writerow({'id':id,'URL':self.current_url,'headline':title.text,'Author':author[0].text,'date':date})
                    database.execute("INSERT INTO article VALUES ({},'{}','{}','{}','{}')".format(id,self.current_url,title.text,author[0].text,date))
                    database.commit()
                    oldtitle = title
                    id += 1
                    continue
                else:
                    continue
            except NoSuchElementException:
                pass
            except KeyboardInterrupt:
                print("Keyboard interrupted")
                sys.exit()
    def date(self,dt):
        month = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        dt = dt.split(", ")
        dt = dt[0].split(" ")+dt[1:2]
        dt = dt[2]+'/'+str(month[dt[0]])+'/'+dt[1]
        return dt
                
                
obj = automate()
obj.getdetails()