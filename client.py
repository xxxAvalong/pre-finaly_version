# Import all needed libraries
from pyfiglet import Figlet
from sys import exit

# And all function from my own created libraries
from put_post import *
from show_post import *
from editor_ import *


def main():
    """
    This is the main function that combines
    all the sub-functions in one place.
    """
    # Creating a preview
    preview_text = Figlet(font='slant')
    print(preview_text.renderText('Welcome:)'))  # Show preview with text

    # Greeting with confirmation of entry.
    entry_confirmation = input('Hi, this is Python microservice "name"'
                               '\nPress "e" to continue, or other key to exit :\n>> ')
    if entry_confirmation.lower().startswith('e'):  # If entry is confirmed

        while True:  # Main cycle with task selection.
            operation = input('\nPlease select a target operation :'
                              '\n1 - Put the post.'
                              '\n2 - Show the post.'
                              '\n3 - Remove post.'
                              '\n4 - Edit post.'
                              '\n>> ')

            if operation in ['1', '2', '3', '4']:  # If input symbol is in task list

                if operation == '1':
                    post = crete_post()  # Function to creation new post
                    send_to_the_server(post)  # Function to send post to the server(Save new post as .txt file)

                elif operation == '2':
                    search_and_show()  # Function to show posts/user_posts based on id/userId

                elif operation == '3':
                    remove_(validation_mod=False)  # Function to  remove post  based on id
                    # Without validation in this case, but it might be used for safety in task with another requests.

                elif operation == '4':
                    edit(validation_mod=False)  # Function to  edit post  based on id
                    # Without validation in this case, but it might be used for safety in task with another requests.

            elif operation.lower().startswith('q'):  # If 'q' was input
                print('Bye :)')
                exit()  # Exit the script

            else:  # Input symbol isn't in task list(and this isn't 'q')
                continue  # Repeat the cycle to ask again

    else:  # Entry was not confirmed
        exit()  # Exit the script


if __name__ == "__main__":  # In case of local start-up, start the main() function
    try:
        main()
    except Exception as ex:
        print(ex)
