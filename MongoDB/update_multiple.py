import os
import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from pprint import pprint 

# Import ObjectId from bson package (part of PyMongo distribution) to enable querying by ObjectID
from bson.objectid import ObjectId

# Load config from .env file
load_dotenv()
MONGODB_URI =                                                      "mongodb+srv://matchemongodb:fdPFKrq1ydUbUejI@cluster0.cqypwa0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize the MongoDB client
client = MongoClient(MONGODB_URI)

#get reference to 'bank' collection
db = client.bank

# get reference to 'accounts' collection
account_collection = db.accounts

# Filter
select_account = {"account_type": "checking"}

# Query by ObjectId
set_field = {"$set": {"minimum_balance": 30000000}}

# Write and expression that adds a 'minimum_balance' field to each savings account and sets it value to 30000000
result = account_collection.update_many(select_account, set_field)
print("Documents updated: " + str(result.modified_count))

print("Documents matched: " + str(result.matched_count))
print("Documents matched: " + str(result.modified_count))
pprint(account_collection.find_one(select_account))

client.close()