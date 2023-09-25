from django.contrib.auth import authenticate


def check_credential(user, data):
    if user is None:
        credentials = {
            "username": data["email"],
            "password": data["password"],
        }
    else:
        credentials = {
            "username": user.username,
            "password": data["password"],
        }
    user = authenticate(**credentials)
    if user:
        return user
