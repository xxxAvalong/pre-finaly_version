from server_communication import *

last_id = 0  # Variable for saving the id of the last created post


def crete_post():
    """
    A function for creating a post and containerizing this data.
    The function also performs validation with a function
    that uses the API structure.
    """
    while True:
        # Do validation(mode is passed to create logs):
        validation_ok = validation('create')  # This function return useId is validation is ok,
        # else return False

        if validation_ok:
            user_id = validation_ok  # If validation was successful validation() return valid userId
            # else return False

            # Create dict that will be used as container with post data:
            data_container = {}

            # Get title and add to data container.
            data_container['title'] = input(" Please enter the new post's title: ")

            # Get body and add to data container
            data_container['body'] = input(" Please enter the new post's body: ")

            global last_id
            if last_id == 0:  # If the post is created for the first time
                try:
                    server_ids = api_data()[1]  # Get ids data from Api server
                    server_post_ids = list(server_ids.keys())  # List them

                    # Take the last id and add 1.
                    last_server_post_id = int(server_post_ids[-1]) + 1
                    last_id = last_server_post_id   # Save the actual id of the last post from the server

                    # And add it to the container with post's data

                except Exception as ex:
                    print(ex, '\nYour post was assigned the number 999.')
                    last_server_post_id = 999  # If there is an error - 999 will be added to the container as an id
            else:
                last_server_post_id = last_id + 1  # Add one for new post id to avoid collision
                # in case of synchronization with the server

                last_id = last_id  # Save the new last id of post in system

            data_container['id'] = last_server_post_id

            data_container['userId'] = user_id  # Add userId to the container with post's data

            return data_container  # Return data container

        else:  # Validation is unsuccessful
            cont = input('User id is not valid.\nExit?[y/n] : ')  # Ask to exit
            if cont.lower().startswith('n'):  # If No/no/n - enter again
                continue

            # If xit is confirmed:
            break


def send_to_the_server(data_container):
    """At this point, the information could be sent to the server
        using requests.put(), but since this is a test job,
        I will save it to a txt file next to the script."""
    post_file = f"{data_container['id']}.txt"  # Name of .txt file where new post will be saved

    try:  # Trying save the new post(send to the server)
        with open(post_file, 'w') as file:  # Create a .txt file with the name of the new post id

            # We disassemble the container with data and write it into the file.
            file.write(f'\nid : {data_container["id"]}'  # id of new post
                       f'\nuser : {data_container["userId"]}'  # userId of new post(Post creator's name(Id))
                       f'\ntitle : {data_container["title"]}'  # title of new post
                       f'\nbody : \n{data_container["body"]}')  # body of new post

    except Exception as ex:  # If there is an error
        print(f'Some saving error :\n{ex}')

    else:  # If saving was successful
        print(f"\nYour post was saved as a {post_file}.")

    return True
