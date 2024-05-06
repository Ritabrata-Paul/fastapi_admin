from pymongo import MongoClient

conn = MongoClient("mongodb://localhost:27017/")


db = conn.university_db


collection_name = db["studentdata_collection"]