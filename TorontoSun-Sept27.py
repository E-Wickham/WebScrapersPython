from urllib.request import urlopen
from bs4 import BeautifulSoup

##### Link collector to send crawler to iteratively

import requests

baseurl = 'https://torontosun.com'

headers = {
    'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
}

columnlinks = []

# Pulling the urls from the last 5 pages worth of columns from here: https://torontosun.com/category/opinion/columnists/?from=1
    
for x in range(11,100,25):
    r = requests.get(f'https://torontosun.com/category/opinion/columnists/?from={x}')
    soup2 = BeautifulSoup(r.content, 'lxml')
    columnlist = soup2.find_all('div', class_='article-card__details')
    for item in columnlist:
            for link in item.find_all('a', href=True):
                columnlinks.append(baseurl + link['href'])

print('Collecting newscolumn links. Beep Boop.')

fPostLink = 'https://torontosun.com/category/national/'
gPostLink = 'https://torontosun.com/category/news/'
hPostLink = 'https://torontosun.com/category/local-news/'
iPostLink = 'https://torontosun.com/category/news/provincial/'
jPostLink = 'https://torontosun.com/category/provincial/'
kPostLink = 'https://torontosun.com/category/world/'
lPostLink = 'https://torontosun.com/category/sports/'
mPostLink = 'https://torontosun.com/category/toronto-maple-leafs/'

for elem in list(columnlinks):
    if elem == "https://torontosun.com/category/columnists/":
        columnlinks.remove(elem)
    elif elem == "https://torontosun.com/category/opinion/":
        columnlinks.remove(elem)
    elif fPostLink in elem:        
        columnlinks.remove(elem)
    elif gPostLink in elem:        
        columnlinks.remove(elem)
    elif hPostLink in elem:        
        columnlinks.remove(elem)
    elif iPostLink in elem:        
        columnlinks.remove(elem)
    elif jPostLink in elem:        
        columnlinks.remove(elem)
    elif kPostLink in elem:        
        columnlinks.remove(elem)
    elif lPostLink in elem:        
        columnlinks.remove(elem)
    elif mPostLink in elem:        
        columnlinks.remove(elem)

print('links cleaned, boop boop')        

linkarray = columnlinks

count = 0

for i in range(0, len(linkarray)):
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
    try:
        pubdatescrape = soup.find('span',class_='published-date__since').get_text()
    except AttributeError:
        pubdate = 'Jan 1, 1991'
    else: 
        pubdate = pubdatescrape


    #   author webscrape - if null do not add to the thing (this doesn't work because the thing is already pulled and transferred)
    try:
        author=soup.find('span',class_='published-by__author').get_text()
    except AttributeError:
        print(headline)
        author= str(input('Enter author name for' + headline + '\n' + url +': '))
    
    try:
        splitauthor = author.split(' ', 1)
        authorfname = splitauthor[0]
        authorlnamewhole = splitauthor[1].split(' ', 1)
        authorlname = authorlnamewhole[0]
    except:
        authorfname = author
        authorlname = author

    #number the entry
    count += 1
    print("==== Column #",count)
                                
    print("=====UPLOADING COLUMN PUBLISHED:====== ", pubdate,'\n', authorfname,'\n', authorlname,'\n', headline,)

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
    #paper_id - Toronto Sun = 5
    #headline 
    #publishdate - PUBDATE
    #body_text
    #url

    mycursor2 = mydb.cursor()
    mycursor2.execute("SELECT headline FROM newscolumns")
    colresult = mycursor2.fetchall()

    #placeholder and specific vars
    #entryColumnistID
    paper_id = 5 #TorontoSun
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
        valNewsColumns = (entryColumnistID, paper_id, newHeadline, bodytext, url, entryDateTime)
        mycursor2.execute(sqlNewsColumns, valNewsColumns)
        mydb.commit()
        print('new entry', newHeadline, 'added to the database')
        
    else:
        print("headline already in database, will not add duplicate:", newHeadline)





