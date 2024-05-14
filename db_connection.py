import os
from dotenv import load_dotenv
from pymongo import MongoClient


def main():
    load_dotenv('.env')

    connection_string = os.getenv('URL')
    # Create a MongoClient instance
    client = MongoClient(connection_string)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Access the database
    database = client.get_database("Python_Project")

    return database
