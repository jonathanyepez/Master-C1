# -*- coding: utf-8 -*-
"""
Created on Tue May 19 22:10:03 2020

@author: Jonathan Yepez
"""
def read_Sentiments(file_sentimientos):
    sentiments = open(file_sentimientos)
    values={}
    for line in sentiments:
        term, value = line.split("\t")
        values[term] = int(value)
        #print(values.items())
    return values

