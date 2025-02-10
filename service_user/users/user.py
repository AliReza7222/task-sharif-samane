from bson.objectid import ObjectId
from django.conf import settings
from werkzeug.security import check_password_hash, generate_password_hash


class User:
    collection = settings.DB.users

    @staticmethod
    def create_user(name, email, phone_number, password):
        hashed_password = generate_password_hash(password)
        user_id = User.collection.insert_one(
            {
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "password": hashed_password,
            },
        ).inserted_id
        return str(user_id)

    @staticmethod
    def get_user_by_id(user_id):
        return User.collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_user_by_email(email):
        return User.collection.find_one({"email": email})

    @staticmethod
    def check_password(email, password):
        user = User.get_user_by_email(email)
        if user and check_password_hash(user["password"], password):
            return user
        return None
