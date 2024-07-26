import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load config from .env file
load_dotenv()

# Get MongoDB URI from environment variables
# Uncomment the line below if you are using .env file to load the URI
# MONGODB_URI = os.getenv("MONGODB_URI")

# Use hardcoded URI if not using .env file
MONGODB_URI = "mongodb+srv://matchemongodb:fdPFKrq1ydUbUejI@cluster0.cqypwa0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize the MongoDB client
client = MongoClient(MONGODB_URI)

# List and print database names
for db_name in client.list_database_names():
    print(db_name)

# Close the client connection
client.close()