#libary
import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import pyodbc 
from sklearn import preprocessing
list_href=[]
#input all type cars in true car website
page_http='https://www.truecar.com/used-cars-for-sale/listings/'
#scrap
home_page=requests.get(page_http)
text_home_page=home_page.text
soup=BeautifulSoup(text_home_page,'html.parser')
sells_soup=soup.find_all("a",{"class":"linkable order-2 vehicle-card-overlay"})
count_href=0
for i in sells_soup :
    list_href.append(i['href'])
    count_href+=1
    if count_href==10000 :
        break
#connect to sql server
connect = pyodbc.connect('Driver={SQL Server};'
                      'Server=name your sql server;'
                      'Database=name of DB;'
                      'Trusted_Connection=yes;')
cursor = connect.cursor()
for i in list_href :
    page_http_car='https://www.truecar.com'+i
    car_page=requests.get(page_http_car)
    text_car_page=car_page.text
    soup=BeautifulSoup(text_car_page,'html.parser')
    #Name
    car_soup_name=soup.find("div",{"class":"heading-2"})
    #Model
    car_soup_model=soup.find("div",{"class":"heading-base"})
    #color
    car_soup_color=soup.find_all("p",{"class":"font-size-3"})
    #Mileage
    car_soup_mileage=soup.find("p",{"class":"margin-top-1"})
    #Location
    car_soup_location=soup.find("div" , {"class":"d-flex align-items-center padding-top-1"})
    #Price
    car_soup_price=soup.find("div",{"class":"heading-2 margin-top-3"})
    #make data base
    cursor.execute("INSERT INTO tblInformation(Name,Model,Color,Mileage,Location,Price) VALUES (?,?,?,?,?,?)",(car_soup_name.text,car_soup_model.text,(car_soup_color[1]).text,car_soup_mileage.text,car_soup_location.text,car_soup_price.text))
    connect.commit()
