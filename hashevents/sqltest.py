import twitter, MySQLdb, urllib2, re
from BeautifulSoup import BeautifulSoup
from local_settings import *
from settings import *

def get_title(url):
    response=urllib2.urlopen(url)
    html=response.read()
    soup=BeautifulSoup(html)
    title=soup.title.text
    realurl=response.geturl()
    return title, realurl

#import the twitter module and the twitter api keys 
api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                      consumer_secret=MY_CONSUMER_SECRET,
                      access_token_key=MY_ACCESS_TOKEN_KEY,
                      access_token_secret=MY_ACCESS_TOKEN_SECRET)
                      
#connect and authenticate with the api
#print api.VerifyCredentials()
 
db = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB)
 
#create a cursor for the select
cur = db.cursor()

if HASHTAG[0]=="#":
    tablename=str(HASHTAG[1:])
else: 
    tablename=str(HASHTAG)

test=cur.execute('select * from %s.%s;' % (MYSQL_DB, tablename))
data = cur.fetchall()
    
print data