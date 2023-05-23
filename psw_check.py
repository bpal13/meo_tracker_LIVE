import re


def check_password(password):
    response = None
    if len(password) <= 6:
        response = "Password must be at least 6 characters long."
        return response
    if re.search(r'[A-Z]', password) and re.search(r'[0-9]', password):
        response = True
        return response
    else:
        response = "Password must contain at least one upper case letter and a number"
        return response
