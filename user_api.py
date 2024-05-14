from db_connection import main


class API:
    def __init__(self):
        # Access the collection
        db = main()
        self.collection = db.user_api

    # Insert data into the collection
    def insert_data(self, email: str, api_key: str):
        try:
            data_to_insert = {"email": email, "user_api": api_key}
            result = self.collection.insert_one(data_to_insert)

            if result.acknowledged:
                return "User API inserted successfully."
            else:
                return "Insertion failed."
        except Exception as e:
            return f"An error occurred: {e}"

    def delete_api_key(self, email: str) -> str:
        try:
            delete_query = {"email": email}
            result = self.collection.delete_one(delete_query)

            if result.acknowledged:
                return "User API deleted successfully."
            else:
                return "Deletion failed."
        except Exception as e:
            return f"An error occurred: {e}"
