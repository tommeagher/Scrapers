import twitter, MySQLdb, urllib2
from BeautifulSoup import BeautifulSoup
from local_settings import *

#import the twitter module and the twitter api keys
 
#First, query my db and find the last ID in there
 
api = twitter.Api(consumer_key=MY_CONSUMER_KEY,
                      consumer_secret=MY_CONSUMER_SECRET,
                      access_token_key=MY_ACCESS_TOKEN_KEY,
                      access_token_secret=MY_ACCESS_TOKEN_SECRET)
#connect and authenticate with the api
                      
print api.VerifyCredentials()
 
db = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASS, db=MYSQL_DB)
 
#create a cursor for the select
cur = db.cursor()
 
cur.execute("create table ultracasual_redi.test (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(45))") 
 
#add lines here to query the database. If it's empty, use "None" for since_id
#if the db has items in it, grab the last one and its id and use that for since_id
 
results = api.GetSearch(term="#NICAR13", per_page=100, since_id=None, result_type="recent")
len(results)
results[0].txt
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
 

