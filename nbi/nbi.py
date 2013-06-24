from bs4 import BeautifulSoup
import urllib2
import csv

'''
creates a csv of the schema for National Bridge Inventory
fixed width inspection files. This includes the redundant fields
that need to be cleared out by hand.
'''


url = "http://www.fhwa.dot.gov/bridge/nbi/format.cfm"
response = urllib2.urlopen(url)
readit = response.read()
soup = BeautifulSoup(readit)
table = soup.table

outfile=open("nbischema.csv", "w")
writer=csv.writer(outfile)

body = table.find('tbody')
rows = body.findAll('tr')
for row in rows:
    idtd= row.find('td')
    id = idtd.text.encode('utf-8')
    nametd= idtd.findNext('td')
    name = "_".join(nametd.string.split())
    spam = nametd.findNext('td')
    start = spam.text.split()[0]
    last = spam.findNext('td')
    length = last.text[:last.text.find('/')]
    schema = id, name, start, length
    print schema
    writer.writerow(schema)
    
