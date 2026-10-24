import os
from pymongo import MongoClient

connection_string = os.getenv("MONGODB_URI")

if not connection_string:
    raise RuntimeError("MONGODB_URI is missing from environment")

client = MongoClient(connection_string)

db = client["my_database"]

tasks_collection = db["tasks"]
users_collection = db["users"]


users_collection.create_index("username", unique=True)
users_collection.create_index("email", unique=True)