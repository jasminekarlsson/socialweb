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


def getCategories(reviews):
    businesses = list(set([x['business_id'] for x in reviews]))
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT business_id,category FROM category WHERE business_id IN ('%s')" % ("','".join(businesses)))
    results = cursor.fetchall()
    cursor.close()
    business_cat = {}
    for row in results:
        if row[0] in business_cat:
            business_cat[row[0]].append(row[1]) 
        else:
            business_cat[row[0]] = [row[1]]               
    return business_cat
    
    

def getUserCategories(user, reviews, business_cat):   
    cat_list = []
    for review in reviews:
        if review['user_id'] == user:
            if review['business_id'] in business_cat:
                b = review['business_id']
                cat_list += business_cat[b]
    return cat_list



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

    cursor.execute(query)
    results = cursor.fetchall()
    reviews = []
    for row in results:
        reviews.append(dict(zip(columns,row)))
    random.Random(1300).shuffle(reviews)
    n = int(0.8*len(reviews))
    trainData = reviews[:n]
    testData = reviews [n:]

    user_list = []
    for review in reviews:
            user_list.append(review['user_id'])
    query = "SELECT * FROM friend WHERE user_id IN ('%s')\
            AND friend_id IN ('%s')"% ("','".join(user_list), "','".join(user_list))
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    friendships = set()
    for fr in results:
        tupleFriendship = tuple(fr)
        friendships.add(tupleFriendship)

    Data = cl.namedtuple('Data',['testData','trainingData','friendship'])
    d = Data(testData,trainData,friendships)
    return d

def isFriend(user_id1, user_id2, friendship):
    # for fr in friendship:
    #     if fr[1] == user_id1 and fr[2] == user_id2:
    #         return 1
    # return 0
    if (user_id1, user_id2) in friendship:
        return 1
    return 0

def closeDB():
    db.close()


#fr = isFriend ('oMy_rEb0UBEmMlu-zcxnoQ', 'cvVMmlU1ouS3I5fhutaryQ')
#print fr

#categories1 = getCategories("LJfW5aofHLFzSzB0LGOO8Q")
#categories2 = getCategories('oMy_rEb0UBEmMlu-zcxnoQ')
#print list(set(categories1).intersection(set(categories2)))

#attributes = getAttributes()
#print attributes[3]

#print len(d.trainingData)
#d=getReviews()
#testData = d.testData + d.trainingData
#print len(getCategories(testData))
#print getUserCategories("gVmUR8rqUFdbSeZbsg6z_w", testData, c)
#trainingData = d.trainingData

#for review in testData:
#    print review['stars']
