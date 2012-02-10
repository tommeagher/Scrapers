#1/usr/bin/env python
from mechanize import Browser
from BeautifulSoup import BeautifulSoup

outfile = open("artscraperaw.txt", "w")

mech = Browser()
url = "http://www.jerseyarts.com/OnlineGuide.aspx?searchType=advanced&searchTerm=D%3ad7%3bR%3ar1%2cr2%2cr3%2cr4%3bSp%3a0%3bGc%3a0%3bF%3a0"
page = mech.open(url)

html = page.read()
soup = BeautifulSoup(html)

print >> outfile, soup.prettify()
outfile.close()	
