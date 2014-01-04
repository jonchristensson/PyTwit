 
import re
import time
import http.cookiejar
from http.cookiejar import CookieJar

import difflib

import urllib.request
from urllib.request import urlopen
from urllib.request import HTTPCookieProcessor

from time import gmtime, strftime

import sqlite3

import datetime

### Function to find unique list of list between new and old
def unique_list(newL,oldL):
        outputL=[]
        for item in newL:
                if item not in oldL:
                        outputL.append(item)
        return outputL

def create_db(filename, table_name = 'Cox_tweet'):
        conn = sqlite3.connect(filename, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

        c = conn.cursor()

        # drop specific table in Tweet.db
        c.execute('DROP TABLE IF EXISTS {table_name}'.format(table_name=table_name))
        # Create table
        c.execute('''create table IF NOT EXISTS {table_name}
        (
        time_key datetime
        , create_dt datetime
        , User_ID integer
        , Full_NM text
        , Nick_NM text
        , Tweet text
        )'''.format(table_name=table_name))

        return c

def create_opener():
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept-Language', 'en-US')]
        return opener

def format_tweet(raw_tweet):
        tweet = (re.sub(r'<.*?>', '', raw_tweet))
        tweet = (re.sub('&#39;', "'", tweet))
        tweet = (re.sub('&quot;', '"', tweet))
        tweet = (re.sub('&amp;', 'and', tweet))
        tweet = (re.sub('&#10;', '', tweet))        #new line (enter)
        tweet = (re.sub(r"\\xc3\\xad", 'í', tweet))
        tweet = (re.sub("&nbsp;", '', tweet))        #non breaking space
        tweet = (re.sub(r'\\xc3\\xb3', 'ó', tweet))
        tweet = (re.sub(r"\\xc3\\xa9", 'é', tweet))
        tweet = (re.sub(r'\\xc3\\xa1', 'á', tweet))
        tweet = (re.sub(r'\\xe2\\x80\\x99', "'", tweet))
        tweet = (re.sub(r"\\xe2\\x80\\x98", "'", tweet))
        tweet = (re.sub(r'\\xe2\\x80\\x9c', '"', tweet))
        tweet = (re.sub(r'\\xe2\\x80\\x9d', '"', tweet))
        tweet = (re.sub(r'\\xc3\\xa9', 'é', tweet))
        tweet = (re.sub('&gt', '>', tweet))
        tweet = (re.sub('&lt', '<', tweet))
        return tweet

keyword = 'obama'
twitterSearchUrl = 'https://twitter.com/search?q={keyword}%20lang%3Aen&src=typd&f=realtime'

def main():
        oldTwit = []
        newTwit = []
        OldlistOfListAppend=[]

        c = create_db("Tweets.db")
        opener = create_opener()
        
        howSimAr = [0.5, 0.5, 0.5, 0.5, 0.5] #less numbers, the more reactive

        for i in range(0,2):
                try:
                        print('#######')
                        print('loop',i)
                        allCreate_dt = []
                        allTimeKey = []
                        allFullNM = []
                        allNickNM = []
                        allUserID = []
                        allsplitSourceTop = []
                        listOfList=[]
                        NewlistOfListAppend=[]
                        uniqueList = []
                        uniqueList2 = []
                        delLength=[]

                        create_dt=datetime.datetime.now()
                        create_dt=create_dt.replace(second=0, microsecond=0)

                        sourceCode = str(opener.open(twitterSearchUrl.format(keyword=keyword)).read())
                
                        #Get all the information for each tweet
                        splitSourceAll = re.findall(r'<div class="tweet original-tweet(.*?)id="stream-item-tweet', sourceCode)
                
                        for item in splitSourceAll:
                                #Get the ID of the tweeter
                                splitSourceUserID = re.findall(r'data-user-id="(.*?)"', item)[1]
                                #Get the Full Name of user of the tweet
                                splitSourceName = re.findall(r'<span class="username js-action-profile-name"><s>@</s><b>(.*?)</b>', item)
                                #Get the date of the tweet
                                splitSourceDate = re.findall(r'"tweet-timestamp js-permalink js-nav js-tooltip" title="(.*?)" >', item)
                                #Get only the tweet text
                                splitSource = re.findall(r'<p class="js-tweet-text tweet-text">(.*?)</p>', item)
                                #Identify the top (most popular) tweet in each search
                                splitSourceTop = re.findall(r'<i class=" (.*?)"></i>', item)

                                for item in splitSourceDate:
                                        DateFull = ' '.join(re.findall('- (.*?)$', item)+re.findall('^(.*?) -', item))
                                        time_key = datetime.datetime.strptime(DateFull, '%d %b %y %I:%M %p')

                                for item in splitSource:
                                        aTweet = format_tweet(item)
                                        newTwit.append(aTweet)

                                allUserID.append(splitSourceUserID)
                                allNickNM.append(splitSourceName)
                                allCreate_dt.append(create_dt)
                                allTimeKey.append(time_key)
                                allsplitSourceTop.append(splitSourceTop)

                        for i in range(0,len(newTwit)):
                
                                listOfList=[allUserID[i],allNickNM[i],allTimeKey[i],allCreate_dt[i],newTwit[i], allsplitSourceTop[i]]
                                
                                if listOfList[5] ==['badge-top']:
                                        delLength=len(NewlistOfListAppend)+1        #get location of top-badge to delete later
                                        print('badge top exist')
                                else:
                                        #print('badge top does not exist')
                                        delLength=0
                                
                                #print(listOfList[6])
                                
                                NewlistOfListAppend.append(listOfList)
                        #print('lenght of list before badge top deletion',len(NewlistOfListAppend))
                        print('test')
                        if delLength > 0:
                                del NewlistOfListAppend[delLength-1]
                                del allUserID[delLength-1]
                                del allNickNM[delLength-1]
                                del allTimeKey[delLength-1]
                                del allCreate_dt[delLength-1]
                                del newTwit[delLength-1]        #delete the tweet of the 'top tweet' - the one with badge top on.
                                del allsplitSourceTop[delLength-1]
                                print('badge top deleted')

                        
                        
                        

                        comparison = difflib.SequenceMatcher(None, newTwit, oldTwit)
                        howSim = comparison.ratio()
                        #print('###########')
                        print("This selection is ",howSim,"similar to the past")
                        # print('new tweets',newTwit)
                        # print('old tweets',oldTwit)
                        howSimAr.append(howSim)
                        howSimAr.remove(howSimAr[0])
                        print(howSimAr)

                        waitMultiplier = (sum(howSimAr)/len(howSimAr))

                        #Use function created earlier to grab only new tweets
                        uniqueList = unique_list(NewlistOfListAppend,OldlistOfListAppend)
                        print(uniqueList)
                        print('length of unique list (all)',len(uniqueList))


                        OldlistOfListAppend=[]
                        oldTwit = []
                        uniqueList=[]
                        for eachItem in newTwit:
                                oldTwit.append(eachItem)
                        for eachItem in NewlistOfListAppend:
                                OldlistOfListAppend.append(eachItem)


                        newTwit = []
                        NewlistOfListAppend=[]

                        time.sleep(waitMultiplier*10)                
                
                except Exception as e:
                                        print(str(e))
                                        print('errored in the main try')
                                        time.sleep(555)

                                #finally:

main()
