import twitter, MySQLdb, urllib2
from BeautifulSoup import BeautifulSoup
from local_settings import *
from settings import *

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
tablename=HASHTAG[1:]

try:
    cur.execute('select * from %s.%s;' % (MYSQL_DB, tablename))
except:
    cur.execute('create table %s (id integer primary key auto_increment, created_at datetime not null, twitid integer not null, source text null, twittext text not null, user_id integer not null, user_screen_name text not null, user_name text not null, user_location text null, user_url text null, user_description text null, retweeted text null, retweet_count text null);' % tablename)

#query the database. If it's empty, use "None" for since_id
#if the db has items in it, grab the last one and its id and use that for since_id
try:
    sinceid = cur.execute('select max(twitid) from hashevents.NICAR13;')
except:
    sinceid=None    

##START HERE
#start at pagenum=1, if the len of results is 100, then try it with pagenum=2. Try a while? 
pagenum=1 
 
results = api.GetSearch(term="#NICAR13", per_page=100, since_id=sinceid, page=pagenum, result_type="recent")

if len(results)==100:
    results = 
len(results)
#loop this



text = results[0].txt
earls = re.findall(r'(https?://\S+)', text)
len(earls)

#if len of json is >99, then try page 2 query and add that.
 
#take the items in the json array, process, parse out urls, grab titles
  
def get_title(url):
    response=urllib2.urlopen(url)
    html=response.read()
    soup=BeautifulSoup(html)
    title=soup.title.text
    realurl=response.geturl()
    return title, realurl
 
title, realurl = get_title(url)
 
#and push all info for each tweet and insert into db