#script to read files (each file is a document content in raw json format) from a 
#specified folder and write to a MongoDB collection
#Have mongod.exe and mongo.exe running (in that order) when you execute this code
import os
#using pymongo and json
import pymongo
import json
# Connection to Mongo DB
try:
    conn=pymongo.Connection()
    print "Connected successfully!!!"
except pymongo.errors.ConnectionFailure, e:
   print "Could not connect to MongoDB: %s" % e 
conn

datadir = os.path.join(os.path.abspath('.'), 'data/')

# all files in the data directory
filenames = os.listdir(datadir)

# limit it to the first n files
# filenames = filenames[:5]

# Define my mongoDB database
db = conn.odesk_files

# Define my collection where I'll insert my search
# Get a collection
collection = db.ryan_collection

# process each file sequentially
for fn in filenames:
    with open(datadir + fn,'r') as record:
        data=record.read()
    record.close()
    ##print data to see what is read
    print data
    #insert document into collection
    doc=json.loads(data)
    collection.insert(doc)
