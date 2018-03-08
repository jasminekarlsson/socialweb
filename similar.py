import MySQLdb

db = MySQLdb.connect("localhost","root","pass","yelp_db")
# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT * FROM user"

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      name = row[0]
      # Now print fetched result
      print "name=" + name
except:
   print "Error: unable to fecth data"

# disconnect from server
db.close()
