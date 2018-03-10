import MySQLdb
import collections as cl

#Calculates simularity between given user1 and user2
def calculatSimularity(user1, user2):
    sim = 5 - abs(user1[8] - user2[8])
    # print "Users: " + user1[1] + " and " + user2[1] + " has similarity " + str(sim)
    return sim


def getSimilarity():
    db = MySQLdb.connect("localhost","root","pass","yelp_db")
    db2 = MySQLdb.connect("localhost","root","pass","yelp_db")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor2 = db2.cursor()
    sql = "SELECT * FROM User LIMIT 5000"

    # Execute the SQL command
    cursor.execute(sql)
    # Fetch all the rows in a list of lists.
    results = cursor.fetchall()
    number = 0
    user1 = []
    user2 = []
    similarity = []
    rows = 0
    column = 0
    #Goes through all the users in a nested loop
    for row in results:
        cursor2.execute(sql)
        for rowx in results:
            #Check if user1 and user2 is the same
            if row[0]  == rowx[0]:
                print row[1]
            else:
                # number = number +
                #Append user1, user2 and similarity to 3 different arrays
                user1.append(row[0])
                user2.append(row[0])
                similarity.append(calculatSimularity(row, rowx))

    # Now print fetched result
    # print number
    Data = cl.namedtuple('Data',['user1','user2',"similarity"])
    d = Data(user1,user2,similarity)
    # disconnect from server
    db.close()
    return d

#getSimilarity()
