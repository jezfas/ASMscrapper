#auctions.asm-autos.co.uk car items web scraper
from requests import get
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import csv
import boto3


def lambda_handler(event, context):
    
    car4bids = []
    s3 = boto3.resource('s3')

    #creating empty list variables for data collected to be stored

    for page in range(1,3):

        url = "https://auctions.asm-autos.co.uk/auction/items/?x=0&type=1&tab=1&list=1\
            &section_id=&make=&transmission=0&fuel=0&seller=&category=&location=0&sort=\
                &time=0&distance=0&options=&layout=r50&search=&fp=0&page=" + str(page)

        """looping though all pages in search section,
        store in page and add to search url for unique url for each search page"""

        response = get(url) #request the url, store in response
        searchPage = BeautifulSoup(response.content, "html.parser") #read all url content as html, store in searchPage
        details = searchPage.find_all("div", class_ = "row vehicle_list")

        #find all div elements with class that contains all needed information on each item
        #store in details

        sleep(randint(2,8)) #pauses loop for random secs to control requests


        for cars in details:
            
            item = cars.find("div", class_ = "list_title").text.strip(),
            price2 = cars.find("span", class_ = "list_price_2").text.strip(),
            link = "https://auctions.asm-autos.co.uk" + cars.find("a")["href"],
            time = cars.find("span", id = True).text

            #looing through details finding the needed info within the respective tags and attribute
            #store the info in variables

            if price2 == None:
                continue
            """for some iterations of details, class attriute=list_price_2 isn't there (none)
                the attriute is list_price_3 due to search desgin error as items aren't cars.
                if none ignore"""
                
            carDetails = {
                "Vechile":item, 
                "Price":price2, 
                "Webpage":link, 
                "Countdown":time
            }
            
            car4bids.append(carDetails)

            #appending the text content of info with no whitespaces to matching list variable

    with open('car4bidsdata.csv', 'w') as c4bData:
        fieldnames = ['Vechile','Price','Webpage','Countdown']
        writer = csv.DictWriter(c4bData, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(car4bids)
        
    s3.Bucket('datacollect4asm').upload_file('car4bidsdata.csv', 'car4bidsdata.csv')
    
    return {
        'statusCode':200,
        'body':'Data collected'
    } 
