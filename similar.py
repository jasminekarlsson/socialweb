import MySQLdb
import collections as cl
import json

credential = json.load(open('credential.json'))
host = credential["host"]
user = credential["user"]
password = credential["password"]
db_name = credential["db_name"]

#Calculates simularity between given user1 and user2
def calculatSimularity(user1, user2, reviews):
    sim = 5 - abs(user1[8] - user2[8])
    # # print "Users: " + user1[1] + " and " + user2[1] + " has similarity " + str(sim)
    # db = MySQLdb.connect(host, user, password, db_name)
    # # prepare a cursor object using cursor() method
    # cursors = db.cursor()
    # print "In function 2 " + str(user2[2])
    # sql = "SELECT * FROM Review WHERE user_id=\'" + str(user2[0]) + "'"
    # cursors.execute(sql)
    # results = cursors.fetchall()
    # print "Here comes reviews"
    # equalrews = 0
    # mean = 0
    # for row in results:
    #     for rowx in reviews:
    #         if row[0] == rowx[0]:
    #             equalrews = equalrews + 1
    #             mean = mean + abs(row[3]-rowx[3])
    #
    # if mean == 0:
    #     print "No similar reviews"
    #
    # else:
    #     sim = mean/equalrews
    #     print "New sim = " + sim

    return sim


def getSimilarity():
    db = MySQLdb.connect(host, user, password, db_name)
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor2 = db.cursor()
    cursorrev = db.cursor()
    sql = "SELECT * FROM User LIMIT 500"
    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    user1 = []
    user2 = []
    similarity = []
    #Goes through all the users in a nested loop
    for row in results:
        cursor2.execute(sql)
        sqlrev = "SELECT * FROM Review Where user_id=\'" + str(row[0]) + "'"
        # cursorrev.execute(sqlrev)
        # reviewsu1 = cursor.fetchall
        reviewsu1 = []
        for rowx in results:
            #Check if user1 and user2 is the same
            if row[0]  == rowx[0]:
                print row[1]
            else:
                #Append user1, user2 and similarity to 3 different arrays
                user1.append(row[0])
                user2.append(row[0])
                similarity.append(calculatSimularity(row, rowx, reviewsu1))

    # disconnect from server
    db.close()
    return (user1,user2,similarity)

getSimilarity()
