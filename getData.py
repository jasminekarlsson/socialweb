# -*- coding: utf-8 -*-
"""
Created on Tue Mar 06 14:27:29 2018

@author: Maria
"""

import MySQLdb
import numpy as np
import random
import collections as cl
import json

credential = json.load(open('credential.json'))
host = credential["host"]
user = credential["user"]
password = credential["password"]
db_name = credential["db_name"]

if "lampp" in credential:
    lampp = credential["lampp"]
    db = MySQLdb.connect(user=user,passwd=password,db=db_name,unix_socket=lampp)
else:
    db = MySQLdb.connect(host,user, password, db_name)


def getUsers():
    cursor = db.cursor()
    query ="SELECT id FROM user"
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def getCategories():
    cursor = db.cursor()
    query ="SELECT business_id, category FROM category"
    cursor.execute(query)
    results = cursor.fetchall()
    columns = ['business_id','category']
    categories = []
    for row in results:
        categories.append(dict(zip(columns,row)))
    return categories
    db.close()



def getAttributes():
    cursor = db.cursor()
    query ="SELECT business_id, name, value FROM attribute LIMIT 10"
    cursor.execute(query)
    results = cursor.fetchall()
    columns = ['business_id','name', 'value']
    attributes = []
    for row in results:
        attributes.append(dict(zip(columns,row)))
    return attributes
    db.close()

def getReviews():
    columns = ['id','business_id','user_id','stars','date','text']
    cursor = db.cursor()
    query ="SELECT id,business_id,user_id,stars,date,text FROM review limit 10"
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
    cursor = db.cursor()
    query = """SELECT COUNT(*) FROM friend WHERE user_id = '%s'\
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
