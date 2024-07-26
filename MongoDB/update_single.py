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

# Filter
document_to_update = {"_id": ObjectId('66a315736575b7a9edc80ffd')}

# Query by ObjectId
add_to_balance = {"$inc": {"balance": 100}}

# Print orginal document
pprint(account_collection.find_one(document_to_update))

# Write and expression that adds to the target account balance by the specific ammount
result = account_collection.update_one(document_to_update, add_to_balance)
print("Documents updated: " + str(result.modified_count))

# Print updated doc.
pprint(account_collection.find_one(document_to_update))

client.close()