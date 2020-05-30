# -*- coding: utf-8 -*-
"""
Created on Tue May 19 22:15:30 2020

@author: Jonathan Yepez
"""
#Importing the relevant libraries
import json #library to parse info from a json formatted .txt file
import html #library to convert HTML entities to String html.unescape()
from langdetect import detect #library to detect tweet's language

#Importing libraries and information for NLP
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stpwrds = set(stopwords.words('english')) #Save a set of stopwords in a variable that will be manipulated
stpwrds.add('RT') #add RT to the set of stopwords -> specific for this case RT == ReTweet
stpwrds.add('rt') #lowercase RT
stpwrds.add("n't") #add n't to the set of stopwrods -> shouldn't => [should, n't]

#==============================================================================
#Define the function to read the file Sentimientos.txt
def read_Sentiments(file_sentimientos):
    sentiments = open(file_sentimientos)
    values={}
    for line in sentiments:
        term, value = line.split("\t")
        values[term] = int(value)
    return values
#-----------------
values = read_Sentiments("Sentimientos.txt") #read list of words and values from Sentimientos.txt

#==============================================================================
#Initialize arrays and dictionaries that will be used in the analysis
tweets_arr = [] #create an empty list of tweets that will contain info in json format
tweets = {} #initialize empty tweets dictionary
english_tweets = {} #initialize an empty dict for tweets that are in English
other_tweets = {} #empty dictionary for tweets NOT in English
error_tweets = {} #empty dictionary for tweets that are either empty or are not words
final_values = [] #empty list that will store tuples (tweet, sentiment_value)
#------------------------------------------------------------------------------
with open("Tweets.txt") as f: 
    for i in f: #for every line in the tweets.txt file append it to the tweets list
        tweets_arr.append(json.loads(i))

counter = 0 #initialize counter -> for indexing in the tweets dict
for j in range(len(tweets_arr)): #for every line stored in the tweets list
    if len(tweets_arr[j].keys()) != 1: #if the json dictionary has only one key
                                        #we assume it is NOT a 'tweet object'
        tweets[counter] = tweets_arr[j]["text"] #we save only the info from the 'text' key
        counter += 1

#------------------------------------------------------------------------------
en_count = 0
other_count = 0
err_count = 0
for k in range(len(tweets)): #Now we are going to analyse every tweet's text
    #first we filter by language -> if the text is in english, then we can calculate sentiment
    #if the text is NOT in English we can just set the sentiment value to 0    
    texto = tweets[k]
    try:
        if(detect(texto.lower())=='en'): #if the tweet is in Enlgish
            english_tweets[en_count] = html.unescape(texto) #save the unescaped text in English
            en_count += 1

        else:
            other_tweets[other_count] = html.unescape(texto) #save the unescaped non-english text in other tweets
            other_count += 1
        
    except:
        error_tweets[err_count] = html.unescape(texto) #save the unescaped error text in error_tweets
        err_count += 1

#----------------Function to Calculate Tweet's Sentiment----------------------#

def calc_sent(text):
    sentiment_value = 0 #initialize sentiment value as 0
    #text is the string that corresponds to the tweet
    text = text.split(" ") #we split the string regex:whitespace
    #now we check each workd agains the values dictionary
    for word in text:
        try:
            sentiment_value += values[word.lower()]
            #read something from the values
        except:
            #print("the word is not in the list")
            sentiment_value += 0
    
    #we then save the results in a tuple that will then be stored in the final_values
    #print("the value for this tweet is: "+str(sentiment_value))
    return(sentiment_value)
           
#------------------------------------------------------------------------------
    
#Process English tweets
#print("\nAnalyzing Tweets in Enlgish...\n")
for tweet in english_tweets:
    v = calc_sent(english_tweets[tweet])
    temp = (english_tweets[tweet],v)
    final_values.append(temp)

#Processing tweets that were not considered English text
#print("\nAnalyzing Tweets in other languages...\n")
for tweet in other_tweets:
    v=calc_sent(other_tweets[tweet])
    temp = (other_tweets[tweet],v)
    if(v!=0):
        final_values.append(temp)
        
#=====================FINAL OUTPUT FOR EXERCISE 1==============================
for item in final_values:
    print("EL SIGUIENTE TWEET: '"+item[0]+"' TIENE UN SENTIMIENTO ASOCIADO DE: "+str(item[1]))


############################################################################### 
###############################################################################
               
# Part 2
#para cada tweet, establecer valores para cada palabra que NO este en el listado values

#1. Read the evaluated tweet
#2. Split the tweet
#3. Depur/Clean-Up the tweet
#4. Stop-Words -> value=0
#5. For other words, check if they are in the 'values' dictionary, otherwise
    #assign them a mean sentiment value

#---------------------Function to Clean-Up a word-----------------------------#
        
def cleanWord(word):
    word = word_tokenize(word.lower()) #we tokenize the 'word'
    for w in word: #we try to depur the caracters or substrings that are NOT alphanumeric
        if(w.isalnum()==False and len(w)<=1): #for example when we have hypened words (i.e. pinkish-blue.)
            word.remove(w) #remove substrings or characters that are NOT alpahumeric and may cause confusion         
    return word

#--------------------Function to 'Join' substrings into one-------------------#
    
def joiner(element): #we assume element is a list of 2 or more strings (i.e. ["should","n't"])
    temp=""
    for e in element:
        temp += e #we concatenate strings as they are at that moment
    return temp

#----------------Furnction to caclulate values for 'new' words----------------#

def wordValues(tweet, value): #tweet-> String, #value -> integer
    #we check the number of alphanumeric subelements
    sub_elements=[] #this list will contain a tuple of (element,mean-value)
    flags=[] #list of elements and flags (multiplication factor for mean-value)
    num_alnum = 0 #number of ~alphanumeric elements
    splitted = tweet.split(" ") #we save the splitted text in the variable
    #depured=[] 
    
    for element in splitted: #for every element in the splitted tweet
        
        #we first do a clean-up of the word
        if(len(cleanWord(element))>1):
            temp_element = joiner(cleanWord(element))
        else:
            if(len(cleanWord(element))==0): #if the element is an emoji or a non-alphanumeric, cleanWorld will return an empty list
                temp_element = "" #we then assign an empty string to it
            else:
                temp_element = cleanWord(element)[0] #we access the 0th element because cleanWord returns a list -> from tokenization
        
        #we can now validate: 1) if the element is in the Stop-Words set
        #or 2) if it contains 'useless' info
        
        #print(temp_element)
        
        if(temp_element.isalnum()):
            try: #now we check if the word/element is a key from the values dictionary
                if(values[element.lower()]!=0):
                    num_alnum += 1
                    pass #this would be the case for a word that was used to calculate the first value of sentiment for the tweet
                
            except: #if the element contains some punctuation for example
                try:
                    if(values[temp_element]!=0):
                        flags.append((element,values[temp_element])) #append the element to the flags list and do not consider it for the mean-value calculation
                except:
                    if(temp_element not in stpwrds):
                        if((element.startswith("@") or ("@" in element)) or element.startswith("http")): #the http condition is just in case; however it is not likely to ever happen
                            flags.append((element,0))
                        else:
                            flags.append((element,1))
                            num_alnum += 1
                    else:
                        flags.append((element,0))
                    
        else:
            partial = "".join(filter(str.isalnum,element))
            if((partial.isalnum()) and (partial[:4]!="http") and ("@" not in element)): #if the element is not exactly alpahumeric but has some sense of it then consider it alphanumeric
                flags.append((element,1))
                num_alnum += 1
            else:
                flags.append((element,0))

    if (num_alnum == 0): #if there are no alphanumeric elements in the tweet whatsoever
        mean_value = 0
    else:
        mean_value = round(value/num_alnum,2) #if the value is 0 then the mean value will be 0 too
    
    for flag_element in flags: #now for every tuple in the flags list
        if(flag_element[1]!=(0 or 1)):
            sub_elements.append((flag_element[0],flag_element[1]))
        else:
            sub_elements.append((flag_element[0],(flag_element[1]*mean_value)))
        
    return [sub_elements, num_alnum]        

#=====================FINAL OUTPUT FOR EXERCISE 2==============================

#----------------Furnction to display results for exercise 2------------------#

def displayValues(tweet,sentimentValue):
    [example,n_div]=wordValues(tweet,sentimentValue)
    print("------------------------")
    print("the tweet that will be analyzed is: \n'"+tweet)
    print("the sentiment value for this tweet was: "+str(sentimentValue))
    print("------------------------")
    print("the mean value was obtained by dividing: "+ str(sentimentValue) +" by "+str(n_div))
    print("the results are as follows: \n")

    for line in example:    
            print(line[0],"\t",line[1])

#------------------------------------------------------------------------------
for i in range(len(final_values)):
    #print("Analysis for Tweet: '"+final_values[i][0]+"' \n")
    tweet = final_values[i][0]
    sentiment = final_values[i][1]
    displayValues(tweet,sentiment)
    
    
