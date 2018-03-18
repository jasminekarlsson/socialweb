# -*- coding: utf-8 -*-
"""
Created on Tue Mar 06 14:27:29 2018
@author: Maria
"""

import MySQLdb
#import numpy as np
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
    cursor.close()
    #db.close()
    return results


def getCategories(user):
    cursor = db.cursor()
    query ="""SELECT DISTINCT category FROM category WHERE business_id IN\
            (SELECT business_id FROM review WHERE user_id = '%s')"""%(user)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results
    #db.close()



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
    #db.close()

def getReviews():
    columns = ['id','business_id','user_id','stars']
    cursor = db.cursor()

    query = "SELECT r.id, r.business_id, r.user_id, r.stars\
              FROM review r JOIN business b ON r.business_id = b.id\
              WHERE b.city = 'Hudson' LIMIT 3500"

    # Vaughan

    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    #db.close()
    reviews = []
    for row in results:
        reviews.append(dict(zip(columns,row)))
    random.Random(1300).shuffle(reviews)
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
    cursor.close()
    #db.close()
    return bool(results)

def closeDB():
    db.close()


#fr = isFriend ('oMy_rEb0UBEmMlu-zcxnoQ', 'cvVMmlU1ouS3I5fhutaryQ')
#print fr

#categories1 = getCategories("LJfW5aofHLFzSzB0LGOO8Q")
#categories2 = getCategories('oMy_rEb0UBEmMlu-zcxnoQ')
#print list(set(categories1).intersection(set(categories2)))

#attributes = getAttributes()
#print attributes[3]

#d = getReviews()
#print d.testData[1]
#print len(d.trainingData)

#testData = d.testData
#trainingData = d.trainingData

#for review in testData:
#    print review['stars']
