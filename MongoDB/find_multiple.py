import os
import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pprint import pprint 

# Import ObjectId from bson package (part of PyMongo distribution) to enable querying by ObjectID
from bson.objectid import ObjectId

# Load config from .env file
load_dotenv()
MONGODB_URI =                                                 "mongodb+srv://matchemongodb:fdPFKrq1ydUbUejI@cluster0.cqypwa0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize the MongoDB client
client = MongoClient(MONGODB_URI)

#get reference to 'bank' collection
db = client.bank

# get reference to 'accounts' collection
account_collection = db.accounts

# Query by ObjectId
document_to_find = {"balance": {"$gt": 8000}}

# write an expression that selects the docs. matching the query constraint in the 'accounts' collection
cursor = account_collection.find(document_to_find)

num_docs = 0
for document in cursor:
    num_docs += 1
    pprint(document)
    print()
print("# of documents found: " + str(num_docs))

client.close()