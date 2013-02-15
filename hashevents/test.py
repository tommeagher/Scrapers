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
    tablename=HASHTAG[1:]
else: 
    tablename=HASHTAG

try:
    cur.execute('select * from %s.%s;' % (MYSQL_DB, tablename))
except:
    cur.execute('create table %s (id integer primary key auto_increment, created_at text not null, twitid bigint not null, source text null, twittext text not null, tweeturl1 text null, tweeturltitle1 text null, tweeturl2 text null, tweeturltitle2 text null, tweeturl3 text null, tweeturltitle3 text null, tweeturl4 text null, tweeturltitle4 text null, user_id bigint not null, user_screen_name text not null, user_name text not null, user_location text null, user_url text null, user_description text null, retweeted text null, retweet_count text null);' % tablename)
db.commit()

#query the database. If it's empty, use "None" for since_id
#if the db has items in it, grab the last one and its id and use that for since_id
#How to translate the 1L
cur.execute('select max(twitid) from %s.%s;' % (MYSQL_DB, tablename))
sinceid=cur.fetchone()
if sinceid[0]==None:
    sinceid=None
else:
    sinceid=sinceid[0]

##START HERE
#start at pagenum=1, if the len of results is 100, then try it with pagenum=2. Try a while? 
pagenum=1 
 
results = api.GetSearch(term=HASHTAG, per_page=100, since_id=sinceid, page=pagenum, result_type="recent")
length = len(results)
#print length

while length>99:
    pagenum=pagenum+1
    newres=api.GetSearch(term=HASHTAG, per_page=100, since_id=sinceid, page=pagenum, result_type="recent")
    results=results+newres
    length=len(newres)

newresultslen = len(results)
#print newresultslen    

for result in results:
    created_at=result.created_at
    twitid=result.id
    source=result.source
    twittext=result.text
    user_screen_name=result.user.screen_name
    result_user=api.GetUser(user_screen_name)
    user_id=result_user.id
    user_name=result_user.name
    user_location=result_user.location
    user_url=result_user.url
    user_description=result_user.description
    retweeted=result.retweeted
    retweet_count=result.retweet_count
    earls = re.findall(r'(https?://\S+)', twittext)
    earls_len=len(earls)
#    print earls_len
    if earls_len>0:
        try:
            if earls_len==1:
                tweeturl1, tweeturltitle1 = get_title(earls[0])
                tweeturl2, tweeturltitle2 = None, None
                tweeturl3, tweeturltitle3 = None, None
                tweeturl4, tweeturltitle4 = None, None
            elif earls_len==2:
                tweeturl1, tweeturltitle1 = get_title(earls[0])
                tweeturl2, tweeturltitle2 = get_title(earls[1])
                tweeturl3, tweeturltitle3 = None, None
                tweeturl4, tweeturltitle4 = None, None
            elif earls_len==3:
                tweeturl1, tweeturltitle1 = get_title(earls[0])
                tweeturl2, tweeturltitle2 = get_title(earls[1])
                tweeturl3, tweeturltitle3 = get_title(earls[2])
                tweeturl4, tweeturltitle4 = None, None
            else:
                tweeturl1, tweeturltitle1 = get_title(earls[0])
                tweeturl2, tweeturltitle2 = get_title(earls[1])
                tweeturl3, tweeturltitle3 = get_title(earls[2])
                tweeturl4, tweeturltitle4 = get_title(earls[3])
        except: 
            continue
    else: 
        tweeturl1, tweeturltitle1 = None, None
        tweeturl2, tweeturltitle2 = None, None
        tweeturl3, tweeturltitle3 = None, None
        tweeturl4, tweeturltitle4 = None, None
                
    tuple = (created_at, twitid, source, twittext, tweeturl1, tweeturltitle1, tweeturl2, tweeturltitle2, tweeturl3, tweeturltitle3, tweeturl4, tweeturltitle4, user_id, user_screen_name, user_name, user_location, user_url, user_description, retweeted, retweet_count)        
    print tuple
#START HERE. The insert statement isn't working. That's it.    
#    cur.execute("""INSERT INTO %s.%s VALUES (%s,%s)""",(MYSQL_DB, tablename, created_at, twitid, source, twittext, tweeturl1, tweeturltitle1, tweeturl2, tweeturltitle2, tweeturl3, tweeturltitle3, tweeturl4, tweeturltitle4, user_id, user_screen_name, user_name, user_location, user_url, user_description, retweeted, retweet_count))
#    db.commit()    

#cur.execute("select * from hashtevents.NICAR13")
#rows = cur.fetchall()
#print rows