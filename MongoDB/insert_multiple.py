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

new_accounts = [
    {
        "account_hoder": "James Bond",
        "account_id": "MDB007",
        "account_type": "checking",
        "balance": 100000,
        "last_update": datetime.datetime.utcnow()
    },
    {
        "account_hoder": "Mary Lynn",
        "account_id": "MDB432",
        "account_type": "savings",
        "balance": 234534,
        "last_update": datetime.datetime.utcnow()
    }
]

# write an expression that inserts the 'new_account' document into the 'accounts' collection.
result = account_collection.insert_many(new_accounts)

document_ids = result.inserted_ids
print("# of doucments inserted: " + str(len(document_ids)))
print("_ids of inserted documents: {document_ids}")

client.close()