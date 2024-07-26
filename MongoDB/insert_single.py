import os
import datetime
from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from .env file
load_dotenv()
MONGODB_URI = "mongodb+srv://matchemongodb:fdPFKrq1ydUbUejI@cluster0.cqypwa0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize the MongoDB client
client = MongoClient(MONGODB_URI)

#get reference to 'bank' collection
db = client.bank

# get reference to 'accounts' collection
account_collection = db.accounts

new_account = {
    "account_hoder": "Linus Torvalds",
    "account_id": "MDB123",
    "account_type": "checking",
    "balance": 5035,
    "last_update": datetime.datetime.utcnow()
}

# write an expression that inserts the 'new_account' document into the 'accounts' collection.
result = account_collection.insert_one(new_account)

document_id = result.inserted_id
print("_id of inserted doucment: {document_id}")

client.close()