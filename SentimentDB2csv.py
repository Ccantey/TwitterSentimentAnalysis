import MySQLdb
import re
import csv

infile = open('negative-words.txt', 'r')
##inotherfile = open('positive-words.txt', 'r')

Nwords = infile.readlines() #read the list(technically string) of negative words
infile.close()

Pwords = inotherfile.readlines()
inotherfile.close()

#Set up database, admin@localhost for now
db = MySQLdb.connect(host='127.0.0.1', user='yourUser', passwd='yourPasswd', db='yourDB')
db.set_character_set('utf8')
curr=db.cursor()

#######Query the database for New York City political expressions#######
curr.execute("""SELECT * FROM yourTable WHERE BODY REGEXP 'obama | romney | bloomberg | m.t.a | mta | schumer | nypd | fdny | port | authority | fema | nyoem | mayor | senator | hud | Cuomo | police | transit | njt | nfip | conservtive | conservatives | liberal | liberals | republican | republicans | democrat | democrats'""")
rows = curr.fetchall()

#store tweets
listOfTweets = []
#store negative words in nkeywords
nkeywords = []
#store positive words in pkeywords
##pkeywords = []
#store longitude
X = []
#store latitude
Y = []
#store time
TIME = []

#append Python lists with the appropriate index from MySQLdb
for i in rows:
    listOfTweets.append(i[12])
    X.append(i[10])
    Y.append(i[11])
    TIME.append(i[9])

##for words in neg_words[35:]:
##if using .readlines() returns a list past metadata
##once for negative words
for w in Nwords[35:]:
     nkeywords.append(w.rstrip('\n'))

##once for positive words
for w2 in Pwords[35:]:
    pkeywords.append(w2.rstrip('\n'))
    
#compile method of re matches EXACT expressions
RE_WORD = re.compile(r'\b[a-zA-Z]+\b') 
count = 0
Tweet = []
sentimentEval = []

#Preprocess the tweets to be all lowercase
for k in [x.lower() for x in listOfTweets]:  
    #print "COUNT: ", count
    ncount = 0
    count +=1
    #loop through tweet, check to see if word in tweet is in sentiment lists
    for word in RE_WORD.findall(k): 
        if word in nkeywords:            
            #print 'NEGATIVE', k
            ncount -= 1
 
        if word in pkeywords:            
            #print 'POSITIVE', k
            ncount +=1
    Tweet.append(k)
    #print "TWEET: ", Tweet[-1]
    #print "K: ", k
    sentimentEval.append(ncount)
    #print "SENTIMENT: ", sentimentEval[-1]
    #print "NCOUNT: ", ncount
    #print

output = zip(Tweet, X, Y, TIME, sentimentEval)



writer = csv.writer(open('tweet_sentimentPrePost.csv', 'wb'))
writer.writerows(output)







