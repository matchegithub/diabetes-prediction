#from pymongo import MongoClient

#MONGODB_URI = "mongodb+srv://matchemongodb:fdPFKrq1ydUbUejI@cluster0.cqypwa0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

#client = MongoClient(MONGODB_URI)

#for db_name in client.list_database_names():
#    print(db_name)

#---------------------------------------------------
import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from .env file
load_dotenv()
MONGODB_URI = "mongodb+srv://matchemongodb:fdPFKrq1ydUbUejI@cluster0.cqypwa0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = load_dotenv(MONGODB_URI)

for db_name in client.list_database_names():
    print(db_name)

client.close()

