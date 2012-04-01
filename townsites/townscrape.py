#1/usr/bin/env python
#mechanize acts as an browser to collect html response
from mechanize import Browser
#beautifulsoup lets you strip out the html and parse it through its tree
from BeautifulSoup import BeautifulSoup
#csvkit allows you to output to a csv file easily
from csvkit.unicsv import UnicodeCSVWriter
#re handles regular expressions
import re

#open a csvfile to write to it, set a delimiter and write the header row
outfile = open("sitesdirt.csv", "w")
w = UnicodeCSVWriter(outfile,delimiter=",",encoding="Cp1252")
w.writerow(['name','url'])

mech = Browser()
url = "http://www.state.nj.us/nj/govinfo/county/localgov.html"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)

#look for the section with the id anchorSection, this is the main body of the url listings
for row in soup.findAll('div', {"id" : "anchorSection"}):
#ignore the rows with anchor tags without an href tag
    for anchor in row.findAll('a', href=True):
        name = anchor.string
#give me whatever is in the href call, the actual url of the link
        url = anchor['href'].decode() 
        record = (name, url)
        w.writerow(record)

outfile.close()

#now add a re parser to clean it up for import, stripping out the empty anchors without town names
infile = open("sitesdirt.csv", "r")
outfile = open("townsites.csv", "w")

for line in infile:
#keep the header row
    if re.match("name,url", line):
        print >> outfile,line,    
    if re.findall(".http:", line):
        print >> outfile,line,

infile.close()
outfile.close()