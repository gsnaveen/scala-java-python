from pymongo import MongoClient
userid = urllib.parse.quote_plus('userid')
passWord = urllib.parse.quote_plus('password')
database = 'database'
host = 'yyy.mydomain.com'
port = 27017

try:
    # mongoClient = MongoClient(mongoConnect1)
    mongoClient = MongoClient(host,
                         username = userid,
                         password = passWord,
                         authSource = database,
                         authMechanism = 'SCRAM-SHA-1')
except:
    print("I am unable to connect to the database")

dbCollections = []

#Connect to database
# mongoClient.list_database_names()
dblist = [database]
for db in dblist:
    mongoDB = mongoClient[db]
    for coll in  mongoDB.list_collection_names():
        dbCollections.append([db,coll])
