'''
WEB SCRAPER FOR POINT2HOMES.COM

Pulling new listings for all six major Metropolitan areas
    Toronto
    Montreal
    Vancouver 
    Calgary
    Edmonton
    Victoria
'''

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import date
import re
'''
import mysql.connector

# div class holding each item: class="item-cnt clearfix" (id = unique id per listing)
# address = div class="address-container" (text or data-address)
# beds = li data-label="Beds"
# property type = class="property-type ic-proptype
# price = div class="price " data-price="$1,199,000 CAD" (will need to sort out price with regex, conv to integer)
'''
headers = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
for i in range(1,10,1):

    url = 'https://www.point2homes.com/CA/Real-Estate-Listings.html?location=Toronto%2C+ON&search_mode=location&page={}&sort_by=DESC_listing_created&SelectedView=listings&LocationGeoId=783094&location_changed=&ajax=1'.format(i)

    req = Request(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'})

    html = urlopen(req)
    soup = BeautifulSoup(html.read(), 'html.parser')

    listing = soup.findAll('div', 'item-right-cnt')
    i = 0

    for item in listing:
        try: 
            address = item.find('div',"address-container").text
            price = item.find("div", "price").get_text()
            beds = str(item.find("li", "ic-beds"))
            linkUrl = str(item.find("a", "btn-secondary btn-lg"))
            beds = beds.split('<strong>', 1)
            bedSplit = beds[1].split('</strong>', 1)
            i = i + 1
            address = re.sub(' +', ' ', address)
            price = re.sub(' +', ' ', price)
            date = date.today()
            '''
             #DB information to connect to localhost

            mydb = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="root",
            database ="RealEstateListing"
            )

            #Get everything from the columnist table

            mycursor = mydb.cursor()

            mycursor.execute("SELECT * FROM RealEstateListing")
            result = mycursor.fetchall()

            #check if the listing matches any of the existing listings
            #give listing id to existing listing

            for x in range(0,len(result)):
                if listingName in result[x]:
                    listingID = x+1
                    newListing = False
                    break
                    
                else: 
                    listingID = len(result)+1
                    newListing = True

        #if the name of the new listing does not exist in the  table, add it to the table
            if newListing == True:
                print('name does not exist in record. Creating new Listing ID:')
                sqlListing = "INSERT INTO RealEstateListing (date, address, price, beds) VALUES (%s, %s, %s, %s)"
                valListing = (date, address, price, bed)

                mycursor.execute(sqlListing, valListing)
                print("Adding to database: ", address)
                mydb.commit()
            else:
                print(address, "exists in record under id#: ", listingID) ''' 

            print("/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/")
            print("Entry #" + str(i), "\n", date , "\nBeds: ", bedSplit[0], address, price)
            print(linkUrl)

        except: 
            pass


