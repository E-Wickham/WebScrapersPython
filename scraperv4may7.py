from urllib.request import urlopen
from bs4 import BeautifulSoup

##### Link collector to send crawler to iteratively

import requests

baseurl = 'http://nationalpost.com'

headers = {
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

columnlinks = []

# Pulling the urls from the last 5 pages worth of columns from here: https://nationalpost.com/category/opinion/?from=1
    
for x in range(156,200,25):
    r = requests.get(f'https://nationalpost.com/category/opinion/?from={x}')
    soup2 = BeautifulSoup(r.content, 'lxml')
    columnlist = soup2.find_all('div', class_='article-card__details')
    for item in columnlist:
            for link in item.find_all('a', href=True):
                columnlinks.append(baseurl + link['href'])


#remove this string  from array columnlinks['http://nationalpost.com//category/opinion/']

fPostLink = 'https://financialpost.com/'

for elem in list(columnlinks):
  if elem == "http://nationalpost.com/category/opinion/":
    columnlinks.remove(elem)
  elif fPostLink in elem:        
    columnlinks.remove(elem)
        

linkarray = columnlinks

count = 0

for i in range(0, len(linkarray)):

    count += 1

    url = linkarray[i] # this variable imports into Database under newsColumns
    html = urlopen(url)
    soup = BeautifulSoup(html.read(), 'html.parser')
##### CLEAN WEBSCRAPE OF ALL PERTINENT INFORMATION ######
    ps = soup.find_all('p')
    bodyarray = []
    bodytext = ""

    #   collect all p tags then append all text items to array - then add all items into bodytext string var 
    for p in ps:
        ptext = p.get_text()
        bodyarray.append(ptext)

    for item in bodyarray:
        bodytext += item
        
    #   headline webscrape
    headline = soup.find('h1').get_text()

    #   publish date webscrape
    pubdatescrape = soup.find('span', "published-date__since").get_text()

    if pubdatescrape == None:
        pubdate = ""
    else:
        pubdate = pubdatescrape

    #   author webscrape - if null do not add to the thing (this doesn't work because the thing is already pulled and transferred)
    author = soup.find('span', "published-by__author").get_text()
    if author == "":
        authorfname = ""
        authorlname = ""
    else:
        splitauthor = author.split(' ', 1)
        authorfname = splitauthor[0]
        authorlnamewhole = splitauthor[1].split(',', 1)
        authorlname = authorlnamewhole[0]

                                
    print( count,". =====UPLOADING COLUMN PUBLISHED:====== ", pubdate,'\n', authorfname,'\n', authorlname,'\n', headline,)

    ######      BEGIN INSERT DATA INTO DATABASE     #####

    import mysql.connector
    import re

    #DB information to connect to localhost

    mydb = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="root",
    database ="columnwatcher"
    )

    #get everything from the columnist table

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM columnists")
    result = mycursor.fetchall()

    #check if the first and last name of the columnist matches any of the existing columnists, columnist id = 

    #give columnist id to existing columnist, attribute id to new columnist

    for x in range(0,len(result)):
        if authorfname in result[x] and authorlname in result[x]:
            entryColumnistID = x+1
            newColumnist = False
            break
            
        else: 
            entryColumnistID = len(result)+1
            newColumnist = True

    #if the name of the new columnist does not exist in the columnist table, add it to the table
    if newColumnist == True:
        print('name does not exist in record. Creating new Columnist ID:')
        sqlColumnists = "INSERT INTO columnists (first_name, last_name) VALUES (%s, %s)"
        valColumnists = (authorfname, authorlname)

        mycursor.execute(sqlColumnists, valColumnists)
        print("Adding to database: ", authorfname, authorlname)
        mydb.commit()
    else:
        print(authorfname, authorlname,"exists in record under id#: ", entryColumnistID)

    ##-- insert article --##

    #columnist_id - auto incremented
    #paper_id - National Post is 1 
    #headline 
    #publishdate - PUBDATE
    #body_text
    #url

    mycursor2 = mydb.cursor()
    mycursor2.execute("SELECT headline FROM newscolumns")
    colresult = mycursor2.fetchall()

    #placeholder and specific vars
    #entryColumnistID
    paper_id = 1 #NationalPost
    newHeadline = headline

    import datetime
    #switch PUBLISH DATE to YYYY-mm-dd
    f = '%b %d, %Y'
    entryDateTime = datetime.datetime.strptime(pubdate, f)


    #try 2 on newscolumn insert

    for x in range(0,len(colresult)):
        if newHeadline in colresult[x]:        
            newColumn = False
            break
            
        else: 
            newColumn = True



    #if this headline does not already exist, add it to my database please
    if newColumn == True:
        print('headline does not exist in record. Creating new Column entry')
        sqlNewsColumns = "INSERT INTO newscolumns (columnist_id, paper_id, headline, body_text, url, publishdate) VALUES (%s, %s, %s, %s, %s, %s)"
        valNewsColumns = (entryColumnistID, 1, newHeadline, bodytext, url, entryDateTime)
        mycursor2.execute(sqlNewsColumns, valNewsColumns)
        mydb.commit()
        print('new entry', newHeadline, 'added to the database')
        
    else:
        print("headline already in database, will not add duplicate:", newHeadline)

        # leaving off -> need to figure out a way to convert publish date into DATE format in SQL, 
        # may involve heavy if statement Jan, feb, march etc DONE
        # 1 FIGURED THAT OUT BUT NOW NEED TO CHANGE DATABASE TO ACCEPT DATETIME INPUT / check to see if date time is acceptable DONE
        # 2 TEST INPUT TO NEWSCOLUMNS database (%s - what means) DONE
        #       ENSURE THE SCRIPT WILL NOT INPUT DUPLICATES DONE
        #   TEST WITH REAL ARTICLE
        # 3 set up finding links / loop to skip financial post link (this will have to be in the area where the links are pulled directly)
        # 4 combine database entry script to the webscraper. 



print('===SCRAPE COMPLETE===')