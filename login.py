from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os
from dotenv import load_dotenv

load_dotenv('.env')


class MongoDB:
    def __init__(self):
        connection_string = os.getenv('URL')
        # Create a MongoClient instance
        client = MongoClient(connection_string)

        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        # Access the database
        db = client.get_database("Python_Project")

        # Access the collection
        self.collection = db.login_data

    # Insert data into the collection
    def insert_data(self, username: str, email: str, passkey: str, password: str):
        try:
            # Check if username or email already exists
            existing_user = self.collection.find_one({"email": email})
            if existing_user:
                return "User email already exists."

            # Data is unique, proceed with insertion
            data_to_insert = {"username": username, "email": email, "passkey": passkey, "password": password}
            result = self.collection.insert_one(data_to_insert)

            if result.acknowledged:
                return "Data inserted successfully."
            else:
                return "Insertion failed."
        except Exception as e:
            return f"An error occurred: {e}"

    # Retrieve data from the collection
    def check_user(self, email: str, password: str):
        # Check if a document with the provided email and password exists
        user = self.collection.find_one({"email": email, "password": password})

        if user:
            name = user['username']
            email = user['email']
            return name, email
        else:
            return None, None
