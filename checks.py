import re


def check_password(password):
    '''Password requirements checker:
        -must be at least 6 characters long
        -must contain at leas one upper case letter
        -must contain at least  one number

        Checks the input for the reqs and outputs either 'True' or an error message'''
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


def get_status_data(tools):
    ''' Count the tools based on their status in the DB '''

    labels = ["Kalibrált", "Lejárt kalibrálás",
              "Kalibrálás hamarosan lejár", "Selejt"]
    data = [0, 0, 0, 0]
    for row in tools:
        if row.status == labels[0]:
            data[0] += 1
        elif row.status == labels[1]:
            data[1] += 1
        elif row.status == labels[2]:
            data[2] += 1
        elif row.status == labels[3]:
            data[3] += 1

    return (labels, data)


# TODO Finish the function
def get_location_data(tools):
    ''' Count tools based on their location '''
    labels = []
    data = []

    return (labels, data)
