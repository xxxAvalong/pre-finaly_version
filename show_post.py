from os import path, listdir

from server_communication import *


def search_and_show():
    """
    The function is used to search for posts by id or UserId.
    In the case of a userId search, it looks for all user's posts saved in the system.
    When searching criterion is id, it first searches in the system, then in the server(API).

    If something is searched use function to show(/show and search).
    """

    while True:
        find_mode = input('Select a search criterion :'  # Get search criterion
                          '\n1 - userId.'
                          '\n2 - id.\n>>')
        if find_mode in ['1', '2']:  # If it fits our conditions
            # The target_id can be, depending on the mode: userId or id(respectively)

            target_id = input(f'\nEnter {"userId" if find_mode == "1" else "id"} to find :\n>>')
            if target_id == 'q':
                break

            # If search criterion is userId target files are all post's files in the script path
            # (.txt format  files where file name is number)
            all_posts_files = [file for file in listdir() if str(file).split('.')[0].isdigit()]

            # If search criterion is id, the target file is : one file that's format is .txt and file name is target_id
            target_files = all_posts_files if find_mode == '1' else f"{target_id}.txt"

            success_marker = False  # Marker of something found

            if find_mode == '1':  # If search criterion is userId

                for file in target_files:  # For matching files have

                    with open(file, 'r+') as f:  # Open probably the right file
                        file_content = f.readlines()  # Read them

                        for row in file_content:  # Line by line

                            target_row = f'user : {target_id}'  # Marker that this post have right userId we need
                            if row.strip() == target_row:
                                success_marker = True  # Right post is found

                                for r in file_content:  # Print the right post line by line
                                    print(r, end='')
                                print('\n')

            elif find_mode == '2' and path.exists(target_files):  # If search criterion is id
                # and post in the system(path)

                success_marker = True  # Right post is found

                target_post = open(target_files, 'r')  # Open the post file
                print('\nFound:\n', target_post.read())  # Print read post
                target_post.close()  # Close the post file

            elif find_mode == '2' and not path.exists(f"{target_id}.txt"):  # If search criterion is id
                # and post NOT in the system(path)

                data = api_data()  # Connection and get data about userIds and ids from API(server)
                ids = data[1]  # Ids it's second element from server data list: ({userIds}, {ids})

                if target_id in ids.keys():  # If ids dictionary with data from server have this post's id on the keys
                    success_marker = True  # Right post is found

                    target = ids[target_id]  # Post is value from dictionary with ids as keys
                    # On format: {'post_id': 'post_content'}. And we get the target post content from this dictionary

                    show_and_save_post(target, target_id)  # Show the target post and save it as id.txt

            if success_marker:
                input('\nPress eny key to continue...')  # Delay for user to see the results
                break

            # If there is no post with same userId
            # in the system or there is not any post with tha same user id on the system and on the server - Print it:
            print(f"There is no post{'s in the system'if find_mode=='1' else ''} "
                  f"with this {'userId'if find_mode=='1' else 'id'} :(")

            cont = input('Exit[y/n] : ')  # Ask to exit
            if cont.lower().startswith('n'):  # If No/no/n - ask for search criterion again
                continue

            break
        elif find_mode == 'q':  # Exit function to main menu
            break

        # Case: Find_mode is not '1' or '2':
        continue


def show_and_save_post(target, id_, save=True):
    """
    Function for displaying (printing) data containers
    (in python dictionary format) of posts. Format :
    [{'id': 'post's id', 'userId': 'post's userId', 'title': 'post's title', 'body': 'post's' body}].

    In this program uses with parameter save==True(Saving post's content is activ)
    it is also possible to use this function without further saving of post's content.
    """
    print("\nTarget post :")
    for post in target:  # For every post in the list of posts
        data = (f"\nid : {post['id']}"
                f"\nuser : {post['userId']}"
                f"\ntitle : {post['title']}"
                f"\nbody : \n{post['body']}")
        print(data + '\n')

        if save:  # If save mode is active

            # Write it to the .txt file what's name is post's id.
            with open(f'{id_}.txt', 'w')as f:
                f.write(data)
