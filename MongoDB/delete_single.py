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
document_to_delete = {"_id": ObjectId('66a3130b36c9d4e2f710684d')}

# Search for doc b4 delete
print("Searching for target document before delete: ")
pprint(account_collection.find_one(document_to_delete))

# Write and expression that adds to the target account balance by the specific ammount
result = account_collection.delete_one(document_to_delete)
                                       
#Serach for document after delete                                    
print("Searching for target document after delete: ")
pprint(account_collection.find_one(document_to_delete))

print("Documents deleted: " + str(result.deleted_count))

client.close()