# -*- coding: utf-8 -*-
"""
Created on Tue May 19 22:15:30 2020

@author: Jonathan Yepez
"""
import readSentimientos #file that reads Sentimientos.txt
import json #library to parse info from a json formatted .txt file
import html #library to convert HTML entities to String html.unescape()
from langdetect import detect #library to detect tweet's language

values = readSentimientos.read_Sentiments("Sentimientos.txt") #read list of words and values from Sentimientos.txt
#------------------------------------------------------------------------------
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

en_count = 0
other_count = 0
err_count = 0

for k in range(len(tweets)): #Now we are going to analyse every tweet's text
    #first we filter by language -> if the text is in english, then we can calculate sentiment
    #if the text is NOT in English we can just set the sentiment value to 0    
    texto = tweets[k]
    #print("analysing tweet number: " + str(k))
    try:
        if(detect(texto.lower())=='en'): #if the tweet is in Enlgish
            #temp = html.unescape(texto).split(" ")
            english_tweets[en_count] = html.unescape(texto) #save the unescaped text in English
            en_count += 1

        else:
            #print("----string in another language----")
            #temp = html.unescape(texto).split(" ")
            other_tweets[other_count] = html.unescape(texto) #save the unescaped non-english text in other tweets
            other_count += 1
            #print("--------")
            
        
        #print(k,texto)
        
    except:
        #print("there was an error with the text")
        error_tweets[err_count] = html.unescape(texto) #save the unescaped error text in error_tweets
        err_count += 1
        
        
    #texto = texto.split(" ")
    #print(i, texto)
    
#----------------Function to Calculate Sentiment Value------------------------#
    
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
#index = 0
print("\nAnalyzing Tweets in Enlgish...\n")
for tweet in english_tweets:
    v = calc_sent(english_tweets[tweet])
    temp = (english_tweets[tweet],v)
    #print("EL SIGUIENTE TWEET: '"+english_tweets[tweet]+"' TIENE UN SENTIMIENTO ASOCIADO DE: "+str(v))
    final_values.append(temp)


print("\nAnalyzing Tweets in other languages...\n")
for tweet in other_tweets:
    v=calc_sent(other_tweets[tweet])
    temp = (other_tweets[tweet],v)
    #print("EL SIGUIENTE TWEET: '"+other_tweets[tweet]+"' TIENE UN SENTIMIENTO ASOCIADO DE: "+str(v))
    if(v!=0):
        final_values.append(temp)
        
for item in final_values:
    print("EL SIGUIENTE TWEET: '"+item[0]+"' TIENE UN SENTIMIENTO ASOCIADO DE: "+str(item[1]))
    
                
# Ejercicio 2
#para cada tweet, establecer valores para cada palabra.

def wordValues(tweet, value): #tweet-> String, #value -> integer
    #we check the number of alphanumeric subelements
    sub_elements=[] #this list will contain a tuple of (element,flag,median_value)
    flags=[]
    num_alnum = 0 #number of ~alphanumeric elements
    splitted = tweet.split(" ") #we save the splitted text in the variable
    for element in splitted: #for every element in the splitted tweet
        if(element.isalnum()):
            try: #now we check if the word/element is a key from the values dictionary
                if(values[element.lower()]!=0):
                    num_alnum += 1
                    pass
                
            except: 
                num_alnum += 1
                flags.append((element,1))
                
        else:
            if(("".join(filter(str.isalnum,element))).isalnum() and (("".join(filter(str.isalnum,element)))[:4]!="http")): #if this element has some punctuation 
                                                                                                                            #we also consider it to be almost alphanumeric
                                                                                                                            #and if it is not a URL
                
                num_alnum +=1
                flags.append((element,1)) #we set the flag for the element to 1
            
            else:
                flags.append((element,0))
                
    if (value != 0):
        mean_value = round(num_alnum/value,2)
    else:
        mean_value = 0
        
    for flag_element in flags: #now for every tuple in the flags list
        sub_elements.append((flag_element[0],(flag_element[1]*mean_value)))
        
    return sub_elements        
         

example = wordValues(final_values[1][0],final_values[1][1])
for line in example:
    print(line[0],"\t",line[1])