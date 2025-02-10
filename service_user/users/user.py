import uuid

from django.conf import settings
from werkzeug.security import check_password_hash, generate_password_hash


class User:
    collection = settings.DB.users

    @staticmethod
    def create_user(name, email, phone_number, password):
        user_id = str(uuid.uuid4())
        User.collection.insert_one(
            {
                "user_id": user_id,
                "name": name,
                "email": email,
                "phone_number": phone_number,
                "password": generate_password_hash(password),
            },
        )
        return user_id

    @staticmethod
    def get_user_by_id(user_id):
        return User.collection.find_one({"user_id": user_id})

    @staticmethod
    def get_user_by_email(email):
        return User.collection.find_one({"email": email})

    @staticmethod
    def check_password(email, password):
        user = User.get_user_by_email(email)
        if user and check_password_hash(user["password"], password):
            return user
        return None
