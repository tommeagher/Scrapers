#!/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

outfile = open("nicarscraped.txt", "w")

mech = Browser()
url = "http://ire.org/conferences/nicar-2012/schedule/"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)

for row in soup.findAll('h3', {"class" : "title3"}):
    name = row.find('a').string
    speaker = name.findNext('p')
    subtree = speaker.strong
    subtree.extract()
    speaker2 = speaker.string
    place = row.findNext('div', {"class" : "col-15 meta"}).p.string
    time = place.findNext('p').string
    record = (name, speaker2, place, time)
    print >> outfile, "; ".join(record)
#    print "; ".join(record)

outfile.close()