#!/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
from csvkit.unicsv import UnicodeCSVWriter
import re

# This creates the csv file using the csvkit module and writes to it, creating the header rows
outfile = open("ire12scraped.csv", "w")
w = UnicodeCSVWriter(outfile,delimiter=";",encoding="Cp1252")
w.writerow(['Title','Speaker','Place','Day','Time','Description'])

#Open a browser and fetch the http response from the url
mech = Browser()
url = "http://ire.org/events-and-training/event/20/"
page = mech.open(url)

#read the url and parse it using Beautiful soup
html = page.read()
soup = BeautifulSoup(html)

#The first day of the conference is a Wednesday, or 2, since the list starts counting at 0. 
day = 2
days =[ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
       'Sunday' ]

#find the "ul class 'listview pane'" which wraps around each day's schedule and parse the items in it.
for row in soup.findAll('ul', {"class" : "listview pane"}):
    for row in row.findAll('h3', {"class" : "title3"}):
        name = row.find('a').string
        speaker = name.findNext('p')
        descall = speaker.findNext('p')
        desc = descall.findNext('p').contents[0].string
        subtree = speaker.strong
        if subtree == None:
            speaker2 = None
        else: 
            print subtree
            subtree.extract()
            speaker2 = speaker.string
            speaker2 = speaker2.strip()
#        print speaker2
        place = row.findNext('div', {"class" : "col-15 meta"}).p.string
        time = place.findNext('p').string
        dayofweek = days[day]
        record = (name, speaker2, place, dayofweek, time, desc)
#write the record for the single class to the csv
        w.writerow(record)
#at the end of each day's ul item, add 1 to the day of the week and loop through it again.
    day = day + 1

#always remember to close the file at the end to save it properly    
outfile.close()