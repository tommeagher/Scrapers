#!/usr/bin/env python
from mechanize import Browser
from datetime import date, timedelta
from BeautifulSoup import BeautifulSoup
from csvkit.unicsv import UnicodeCSVWriter
import re

# This creates the csv file using the csvkit module and writes to it, creating the header rows
outfile = open("nicar14sched.csv", "w")
w = UnicodeCSVWriter(outfile,delimiter=",",encoding="Cp1252")
w.writerow(['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location','Private'])

private = False
all_day = False

#Open a browser and fetch the http response from the url
mech = Browser()

#update the URL when you reuse"
url = "http://www.ire.org/conferences/nicar-2014/schedule/"

#update the date of the conference
year = 2014
month = 2
adate = 26
the_date=date(year,month,adate)
page = mech.open(url)

#read the url and parse it using Beautiful soup
html = page.read()
soup = BeautifulSoup(html)

#The first day of the conference is a Wednesday, or 2, since the list starts counting at 0. 
day = 2
days =[ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
       'Sunday' ]
d = timedelta(days=1)

#find the "ul class 'listview pane'" which wraps around each day's schedule and parse the items in it.
for row in soup.findAll('ul', {"class" : "listview pane"}):
    for row in row.findAll('h3', {"class" : "title3"}):
        name = row.find('a').string
        speaker = name.findNext('p')
        descall = speaker.findNext('p')
        desc = descall.findNext('p').contents
        newdesc=""
        for item in desc:
            newdesc += item.string
        desc = newdesc
        subtree = speaker.strong
        if subtree == None:
            speaker2 = None
        else: 
            subtree.extract()
            speaker2 = speaker.string
            speaker2 = speaker2.strip()
        speaker2 = "Speakers: " + speaker2
        place = row.findNext('div', {"class" : "col-15 meta"}).p.string
        time = place.findNext('p').string
        if time == desc:
            desc = None
        else: 
            desc = desc

        mytime = time.split("-")
        start_time=mytime[0].strip()
        if len(start_time.split()[0]) < 3:
            start_time = start_time.split()[0] + ":00:00 " + start_time.split()[1]
        else: 
            start_time = start_time
        end_time=mytime[1].strip()
        if len(end_time.split()[0]) < 3:
            end_time = end_time.split()[0] + ":00:00 " + end_time.split()[1]
        else: 
            end_time = end_time

        dayofweek = str(the_date)
        if desc != None and speaker2 != "Speakers: TBA":
            desc = speaker2 + " - " + desc
        elif desc != None:
            desc = desc
        else: 
            desc = speaker2
        record = (name, the_date, start_time, the_date, end_time, all_day, desc, place, private)

#write the record for the single class to the csv
        w.writerow(record)
#at the end of each day's ul item, add 1 to the day of the week and loop through it again.
    the_date=the_date+d

#always remember to close the file at the end to save it properly    
outfile.close()