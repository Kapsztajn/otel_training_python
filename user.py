import json


def getUser(user):
    return User(
        user_id=user[0],
        email=user[1],
        first_name=user[2],
        last_name=user[3]
    ).to_dict()


class User:
    def __init__(self, user_id, email, first_name, last_name):
        self.user_id = user_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    # Convert the class instance to a dictionary
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    # Convert the class instance to a JSON string
    def to_json(self):
        return json.dumps(self.to_dict())
