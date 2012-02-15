#!/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from csvkit.unicsv import UnicodeCSVWriter

outfile = open("nicarscraped.csv", "w")
w = UnicodeCSVWriter(outfile,delimiter=";",encoding="Cp1252")
w.writerow(['title','speaker','place','time'])

mech = Browser()
url = "http://ire.org/conferences/nicar-2012/schedule/"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)

for row in soup.findAll('h3', {"class" : "title3"}):
    name = row.find('a').string
    speaker = name.findNext('p')
    desc = speaker.findNext('p').nextSibling.string
    subtree = speaker.strong
    subtree.extract()
    speaker2 = speaker.string
    speaker2 = speaker2.strip()
    place = row.findNext('div', {"class" : "col-15 meta"}).p.string
    time = place.findNext('p').string
    record = (name, speaker2, place, time, desc)
    w.writerow(record)
    
outfile.close()