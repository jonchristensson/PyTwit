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
#from datetime import datetime

### Function to find unique list of list between new and old
def unique_list(newL,oldL):
        outputL=[]
        for item in newL:
                if item not in oldL:
                        outputL.append(item)
        return outputL


######################### CREATE DB #############################

conn = sqlite3.connect('Tweets.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
# print('Opened database successfully')

c = conn.cursor()


#drop specific table in Tweet.db
c.execute("DROP TABLE IF EXISTS Cox_tweet")

# # Create table
c.execute('''create table IF NOT EXISTS Cox_tweet_test
(
time_key timestamp
, create_dt timestamp
, User_ID integer
, Nick_NM text
, Tweet text
)''')

# c.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(c.fetchall())
##################################################################



cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0'), ('Accept-Language', 'en-US')]

keyword = '@coxcomm'
startinglink = 'https:/twitter.com/search/realtime?q='

def main():
    oldTwit = []
    newTwit = []
    OldlistOfListAppend=[]

    
    # print(create_dt)

    howSimAr = [0.5, 0.5, 0.5, 0.5, 0.5] #less numbers, the more reactive

    while 1 < 2:
    # for i in range(0,20):
        try:
            print('#######')
            print(datetime.datetime.now())

            # print('loop',i)
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

            #create_dt=strftime("%Y-%m-%d %H:%M:%S")
            create_dt=datetime.datetime.now()
            create_dt=create_dt.replace(second=0, microsecond=0)

            sourceCode = str(opener.open('https://twitter.com/search?q='+keyword+'%20lang%3Aen&src=typd&f=realtime').read())
    
            splitSourceAll = re.findall(r'<div class="tweet original-tweet(.*?)id="stream-item-tweet',sourceCode)        #Get all the information for each tweet
    


            for item in splitSourceAll:

                    splitSourceUserID = re.findall(r'data-user-id="(.*?)"',item)[1]                        #Get the ID of the tweeter
                    splitSourceName = re.findall(r'<span class="username js-action-profile-name"><s>@</s><b>(.*?)</b>',item)                        #Get the Full Name of user of the tweet
                    splitSourceDate = re.findall(r'"tweet-timestamp js-permalink js-nav js-tooltip" title="(.*?)" >',item)                        #Get the date of the tweet
                    splitSource = re.findall(r'<p class="js-tweet-text tweet-text">(.*?)</p>',item)                                #Get only the tweet text
                    splitSourceTop = re.findall(r'<i class=" (.*?)"></i>',item)                        #Identify the top (most popular) tweet in each search

                    

                    for item in splitSourceDate:
                            # DateTime=re.findall('^(.*?) -',item)
                            # DateDate=re.findall('- (.*?)$',item)
                            DateFull=' '.join(re.findall('- (.*?)$',item)+re.findall('^(.*?) -',item))
                            for item in DateFull:
                                    time_key = datetime.datetime.strptime(DateFull, '%d %b %y %I:%M %p')
                                    


                    for item in splitSource:
                                    aTweet = (re.sub(r'<.*?>','',item))
                                    aTweet = (re.sub('&#39;',"'",aTweet))
                                    aTweet = (re.sub('&quot;','"',aTweet))
                                    aTweet = (re.sub('&amp;','and',aTweet))
                                    aTweet = (re.sub('&#10;','',aTweet))        #new line (enter)
                                    aTweet = (re.sub(r"\\xc3\\xad",'í',aTweet))
                                    aTweet = (re.sub("&nbsp;",'',aTweet))        #non breaking space
                                    aTweet = (re.sub(r'\\xc3\\xb3','ó',aTweet))
                                    aTweet = (re.sub(r"\\xc3\\xa9",'é',aTweet))
                                    aTweet = (re.sub(r'\\xc3\\xa1','á',aTweet))
                                    aTweet = (re.sub(r'\\xe2\\x80\\x99',"'",aTweet))
                                    aTweet = (re.sub(r"\\xe2\\x80\\x98","'",aTweet))
                                    aTweet = (re.sub(r'\\xe2\\x80\\x9c','"',aTweet))
                                    aTweet = (re.sub(r'\\xe2\\x80\\x9d','"',aTweet))
                                    aTweet = (re.sub(r'\\xc3\\xa9','é',aTweet))
                                    aTweet = (re.sub('&gt','>',aTweet))
                                    aTweet = (re.sub('&lt','<',aTweet))
                                    
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
            # print(uniqueList)
            # print('length of unique list (all)',len(uniqueList))

###########################################################################
            #Use function to add data to DB

            for j in range(0,len(uniqueList)):
            	c.execute('INSERT INTO Cox_tweet_test(time_key, create_dt , User_ID, Nick_NM, Tweet) VALUES(? ,?, ?, ?, ?)', (uniqueList[j][2],uniqueList[j][3],uniqueList[j][0], str(uniqueList[j][1]),uniqueList[j][4]))
 				
            	# c.execute('INSERT INTO Cox_tweet(time_key, create_dt, User_ID, Nick_NM, Tweet) VALUES(?,?,?,?,? )', (uniqueList[j][2] , uniqueList[j][3] , uniqueList[j][0],uniqueList[j][1],uniqueList[j][4], ))
 				#add rows to table
				# time_key - 2
				# create_dt - 3
				# User_ID - 0
				# Nick_NM - 1
				# Tweet - 4
				#c.execute('''INSERT INTO Cox_tweet(time_key, create_dt, User_ID, Nick_NM, Tweet ) VALUES(?,?)''', (uniqueList[j][3],uniqueList[j][4],uniqueList[j][1],uniqueList[j][2],uniqueList[j][5]))

			# c.execute("SELECT count(time_key) FROM Cox_tweet")
			# print(c.fetchall())

            #drop specific table in Tweet.db
			#c.execute("DROP TABLE IF EXISTS Cox_tweet")

#############################################################################

            OldlistOfListAppend=[]
            oldTwit = []
            uniqueList=[]
            for eachItem in newTwit:
                    oldTwit.append(eachItem)
            for eachItem in NewlistOfListAppend:
                    OldlistOfListAppend.append(eachItem)


            newTwit = []
            NewlistOfListAppend=[]

            time.sleep(waitMultiplier*300)                
        
        except Exception as e:
                                print(str(e))
                                print('errored in the main try')
                                time.sleep(555)

                        #finally:




            


                        
                

main()
#c.execute("DROP TABLE IF EXISTS Cox_tweet")
# c.execute("SELECT * FROM Cox_tweet")
# print(c.fetchall())

# drop specific table in Tweet.db
# c.execute("DROP TABLE IF EXISTS Cox_tweet")