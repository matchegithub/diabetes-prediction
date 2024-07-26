import os
import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Import ObjectId from bson package (part of PyMongo distribution) to enable querying by ObjectID
from bson.objectid import ObjectId

# Load config from .env file
load_dotenv()
MONGODB_URI =                                           "mongodb+srv://matchemongodb:fdPFKrq1ydUbUejI@cluster0.cqypwa0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize the MongoDB client
client = MongoClient(MONGODB_URI)

#get reference to 'bank' collection
db = client.bank

# get reference to 'accounts' collection
account_collection = db.accounts

# Query by ObjectId
document_to_find = {"_id": ObjectId("66a315736575b7a9edc80ffc")}

# write an expression that inserts the 'new_account' document into the 'accounts' collection.
result = account_collection.find_one(document_to_find)
print(result)

client.close()