#!/usr/bin/env python
import urllib2
from datetime import date, timedelta
from BeautifulSoup import BeautifulSoup
from csvkit.unicsv import UnicodeCSVWriter

# This creates the csv file using the csvkit module and writes to it, creating the header rows
outfile = open("nicar15sched.csv", "w")
w = UnicodeCSVWriter(outfile,delimiter=",",encoding="Cp1252")
w.writerow(['Subject','Start Date','Start Time','End Date','End Time','All Day Event','Description','Location','Private'])

private = False
all_day = False

#update the URL when you reuse the script next year
url = "http://ire.org/events-and-training/event/1494/"

#use urllib2 to send a request to the URL and gather the html response
response = urllib2.urlopen(url)
html = response.read()

#read the html and parse it using Beautiful soup
soup = BeautifulSoup(html)

#update the date of the conference
year = 2015
month = 3
adate = 4
the_date=date(year,month,adate)
d = timedelta(days=1)

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
        try:
        	speaker2 = "Speakers: " + speaker2
        except:
        	speaker2 = "Speakers TBA"
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