from database import users_collection
from security import hash_password, verify_password

def create_user(user_data: dict):
    user_data = user_data.copy()
    user_data["password"] = hash_password(user_data["password"])

    result = users_collection.insert_one(user_data)

    return {
        "id": str(result.inserted_id),
        "message": "User created successfully"
    }


def get_user_by_username(username: str):
      return users_collection.find_one({"username": username})


def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)

    if user is None:
        return None

    if not verify_password(password, user["password"]):
        return None

    return user
