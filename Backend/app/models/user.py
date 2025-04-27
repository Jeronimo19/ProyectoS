from app.database import db

class UserModel:
    def __init__(self):
        self.collection = db["users"]  # Una colección llamada "users"

    def create_user(self, user_data):
        return self.collection.insert_one(user_data)

    def get_users(self):
        return list(self.collection.find())
