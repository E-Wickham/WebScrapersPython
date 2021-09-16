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
import re

# Toronto


# div class holding each item: class="item-cnt clearfix" (id = unique id per listing)
# address = div class="address-container" (text or data-address)
# beds = li data-label="Beds"
# property type = class="property-type ic-proptype
# price = div class="price " data-price="$1,199,000 CAD" (will need to sort out price with regex, conv to integer)
headers = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'

url = 'https://www.point2homes.com/CA/Real-Estate-Listings.html?location=Toronto%2C+ON&search_mode=location&page=1&sort_by=DESC_listing_created&SelectedView=listings&LocationGeoId=783094&location_changed=&ajax=1'

req = Request(url , headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'})

html = urlopen(req)
soup = BeautifulSoup(html.read(), 'html.parser')

listing = soup.findAll('div', 'item-right-cnt')


for item in listing:
    address = item.find('div',"address-container").text
    price = item.find("div", "price").get_text()
    address = re.sub(' +', ' ', address)
    price = re.sub(' +', ' ', price)
    print(address)
    print(price)
    # if address = "No address available" remove item from list