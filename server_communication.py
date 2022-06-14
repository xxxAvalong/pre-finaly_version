from requests import get as requests_get
from datetime import datetime


def communication():
    """
    This function is for connecting to the API server.
    :return: False is some error. If all is OK return actual data from server,
             in format: a list with the content from the posts as dictionaries.
    """
    try:  # Try connection to the API server
        link = 'https://jsonplaceholder.typicode.com/posts'
        res = requests_get(link)

        if res.ok:  # If server response is correct(200)
            posts = res.json()  # Convert .json response from server to the list with python dictionaries

        else:  # Server return error code
            posts = []
            print('Response code is :', res.status_code)

    except Exception as ex:  # Some communication error
        posts = []
        print(f'\nSome communication error :\n{ex} \nCheck your Internet connection please.\n', )

    #  If connection to the API server is ok actual data will be returned(!).
    #  If there is some error False will be returned(!).
    return posts


def api_data():
    """
    This function used for tidy up data from API server if there are.
    :return: Tided up data from server or
             False if there are no data from API server.
    """
    # If communication is ok and data from API server is gotten
    server_data = communication()
    if server_data:

        ids = {}  # Dictionary in which ids will be added
        user_ids = {}  # Dictionary in which userIds will be added

        for data in server_data:  # In every dictionary on the list

            ids[f'{data["id"]}'] = [data]  # Collect the content of a post as a value
            # and post as key in the ids dictionary

            # Collect the userId from post content as a key and user's posts as value in the user_id dictionary:
            if str(data['userId']) not in list(user_ids.keys()):  # if key not in the userId dictionary yet
                user_ids[f"{data['userId']}"] = []  # Create key-value(userId - blank list)

                user_ids[f"{data['userId']}"].append(data)  # Add first user's(userId's) post in format:
                # [{'id': 'post's id', 'userId': 'post's userId', 'title': 'post's title', 'body': 'post's' body}]
                # to the blank list
            else:
                user_ids[f"{data['userId']}"].append(data)  # Add other user's posts

        return [user_ids, ids]  # list with dictionaries :)

    else:  # There are no data from server
        return False


def validation(action=None):
    """
    This function is used to verify the validity of the userId
    by searching for it on the server.
    :param action: using for create user login.
    :return: Valid userId if it is valid or False if validation is unsuccessfully.
    """
    try:
        # Get target userId to validation. If there are no digits, there will be an exception
        user_id = int(input('Enter your userId for validation please(only numbers) :\n>>'))

        data = api_data()  # Connection to the API server and get actual data

        if data:  # If there are data from API server
            user_ids = data[0].keys()  # Get list with all usersIds

            # Convert list with userIds to the list with userId in int data type:
            int_user_ids = [int(u_id) for u_id in user_ids]

            # If userId to verification in the list with userIds from the server:
            if user_id in int_user_ids:
                save_the_log(user=user_id, act=action)  # Save login
                print('Validation was successful.')
                return user_id  # Return valid userId

        # If there are no data from API server:
        return False

    except Exception as e:  # In case of entering a non-numeric userId value
        print(e, '\n')
        return False


def save_the_log(user, act):
    """
    This is an optional function that creates a file with user validation data,
    which includes the userId validation time and validation events.
    :param user: user's userId
    :param act: target of validation
    """
    with open('logs.txt', 'a') as logs:
        logs.write(f'\nLogin time : {datetime.now().strftime("%d.%m.%Y %H:%M")}'
                   f'\nUser : {user}'
                   f'\nAction : {act}' + '\n')
