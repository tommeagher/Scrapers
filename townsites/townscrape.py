#1/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re

outfile = open("townsites.csv", "w")

mech = Browser()
url = "http://www.state.nj.us/nj/govinfo/county/localgov.html"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)

for row in soup.findAll('div', {"id" : "anchorSection"}):
    for row in row.findAll('ul'):
        for row in row.findAll('li'):
            for anchor in row.findAll('a', href=True):
                name = anchor.string
                for row in anchor:
                    url = anchor['href'].decode() 
                print >> outfile, name, ",", url

outfile.close()

#now add a re parser to clean it up for import
#outfile2 = open("townsites.csv", "r")

        #for link in row.findAll('a'):
           # print link['href']
           # print url.string
#    street = row.find('div', {"class" : "GuideResultAddress"}).span.string
#    city = street.findNext('span').string
#    record = (name, street, city)
#    print >> outfile, ", ".join(record)

#outfile.close()

