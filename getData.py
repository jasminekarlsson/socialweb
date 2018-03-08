# -*- coding: utf-8 -*-
"""
Created on Tue Mar 06 14:27:29 2018

@author: Maria
"""

import MySQLdb
import numpy as np
import random
import collections as cl


def getUsers():
    db = MySQLdb.connect("localhost","mariahotoiu","copacroz","yelp_db" )
    cursor = db.cursor()
    query ="SELECT id FROM User"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def getCategories():
    db = MySQLdb.connect("localhost","mariahotoiu","copacroz","yelp_db" )
    cursor = db.cursor()
    query ="SELECT business_id, category FROM Category"
    cursor.execute(query)
    results = cursor.fetchall()
    columns = ['business_id','category']
    categories = []
    for row in results:
        categories.append(dict(zip(columns,row)))
    return categories
    db.close()
    


def getAttributes():
    db = MySQLdb.connect("localhost","mariahotoiu","pass","yelp_db" )
    cursor = db.cursor()
    query ="SELECT business_id, name, value FROM Attribute LIMIT 10"
    cursor.execute(query)
    results = cursor.fetchall()
    columns = ['business_id','name', 'value']
    attributes = []
    for row in results:
        attributes.append(dict(zip(columns,row)))
    return attributes
    db.close() 
   
def getReviews():
    db = MySQLdb.connect("localhost","mariahotoiu","pass","yelp_db" )
    columns = ['id','business_id','user_id','stars','date','text']
    cursor = db.cursor()
    query ="SELECT id,business_id,user_id,stars,date,text FROM Review Limit 10"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    reviews = []
    for row in results:
        reviews.append(dict(zip(columns,row)))
    random.shuffle(reviews)
    n = int(0.8*len(reviews))
    trainData = reviews[:n]
    testData = reviews [n:]
    Data = cl.namedtuple('Data',['testData','trainingData'])
    d = Data(testData,trainData)    
    return d


def isFriend(user_id1, user_id2):
    db = MySQLdb.connect("localhost","mariahotoiu","pass","yelp_db" )
    cursor = db.cursor()
    query = """SELECT COUNT(*) FROM Friend WHERE user_id = '%s'\
                AND friend_id = '%s'""" %(user_id1, user_id2)
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return bool(results)





#fr = isFriend ('oMy_rEb0UBEmMlu-zcxnoQ', 'cvVMmlU1ouS3I5fhutaryQ')
#print fr

#categories = getCategories()
#print categories[1]

#attributes = getAttributes()
#print attributes[3]

#d = getReviews()
#testData = d.testData
#trainingData = d.trainingData
#for review in testData:
#    print review['stars']
#def getTraining():
#    d = getReviews(db)
#    return d.Training
#    
#    #return np.random.choice(reviews,int(0.8*len(reviews)))    
#
#def getTest():
#    d = getReviews(db)
#    return d.Test
#    
#trainSet = getTraining()
#print len(trainSet)
#testSet = getTest()
#print len(testSet)
