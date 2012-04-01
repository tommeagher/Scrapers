#1/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from csvkit.unicsv import UnicodeCSVWriter
import re

outfile = open("sitesdirt.csv", "w")
w = UnicodeCSVWriter(outfile,delimiter=",",encoding="Cp1252")
w.writerow(['name','url'])

mech = Browser()
url = "http://www.state.nj.us/nj/govinfo/county/localgov.html"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)

for row in soup.findAll('div', {"id" : "anchorSection"}):
#    for row in row.findAll('ul'):
#    for row in row.findAll('li'):
    for anchor in row.findAll('a', href=True):
        name = anchor.string
        url = anchor['href'].decode() 
        record = (name, url)
        w.writerow(record)

outfile.close()

#now add a re parser to clean it up for import
infile = open("sitesdirt.csv", "r")
outfile = open("townsites.csv", "w")

for line in infile:
    if re.match("name,url", line):
        print >> outfile,line,    
    if re.findall(".http:", line):
        print >> outfile,line,

infile.close()
outfile.close()
