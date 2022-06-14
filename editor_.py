from os import path, remove
from server_communication import *


def editor(mode='edit', validation_mod=True):
    """
    This function is used both to edit a post and to delete it,
    depending on the mode.

    It also uses validation(+ logging of entries) for security.
    """
    if validation_mod:  # If validation is active

        # Create the loop to do validation with repeat option. If validation is successful loop will end
        while True:
            valid_ok = validation(action=mode)  # Mode is passed to create logs
            user_id = valid_ok  # Because function validation() return valid userId
            # if user validation is ok, else return False

            if valid_ok:  # If validation was successful end the loop
                break

            # If validation was not successful
            cont = input('Error : userId is not valid.\nExit?[y/n] : ')  # Ask to exit
            if cont.lower().startswith('n'):  # If entered symbols are: not/Not/no/n.. - repeat the validation cycle
                continue

            return False

    else:
        user_id = ''  # Not used yet, will be added if needed.(If mode is 'edit' and verification is not used)

    while True:
        target_id = input(f'\nEnter post id fo {mode} :\n>>')  # Get the post's id to edit/remove
        post_file = f'{target_id}.txt'  # Create a file name that will contain the post content in the system
        if path.exists(post_file):  # If file with this name exists in the script path(If post is in the system)
            print('Actual post :\n')

            with open(post_file, 'r') as f:  # Open this file fo reading
                for row in f.readlines():
                    row = row.strip()
                    print(row)  # And print post's content line by line

                    # If we need the userId:
                    #           In case of editing the post without validation
                    #           we need userId to write to the post's file(because there is no userId from the user)
                    if mode == 'edit' and not validation_mod and row.startswith('user'):

                        try:
                            # Looking for a string beginning with 'user' and take the second part of it(after ':' )
                            user_id = int(row.split(':')[1].strip())

                        except Exception as e:
                            print(f'{e}\nSome problem with userId from post, try to edit the post with validation.')

            if mode == 'edit':  # If there is editing case

                new_title = input('\nEnter new title please :\n>>')  # Get new title
                new_body = input('Enter new body please :\n>>')  # Get new body

                with open(post_file, 'w') as ff:  # Open post's file for editing for rewriting
                    ff.write(f'\nid : {(int(target_id))}\nuser : {user_id}'
                             f'\ntitle : {str(new_title)}\nbody : \n{str(new_body)}')
                    """
                    Clarification: 
                        If you edit a post with validation, the valid userId 
                        will be written to the edited file, 
                        
                        but if you edit without login validation, 
                        the userId will not be changed in the post's file. 
                    
                    To improve security it is better to use this function with active validation 
                        - the user's userId who enter to the system will be saved to the logs file with marked 'edit' .
                    """
                    break

            elif mode == 'remove':  # If there is remove case(Overall userId is not used in this case)
                confirm = input('\nAre you sure you want to delete this post?[y/n]')  # Asking for confirmation
                # to remove post in the system

                if confirm.lower().startswith('y'):  # If remove is confirmed(Yes/yes/y)
                    remove(post_file)  # Remove the target post
                    break
                else:  # Remove is not confirmed
                    continue

        else:  # Validation is unsuccessful
            cont = input('There is no post in the system with this id.\nExit?[y/n]')  # Ask to exit
            if cont.lower().startswith('n'):  # If No/no/n - enter again
                continue
            else:  # Exit is confirmed
                break

    return False


def edit(validation_mod):
    """
    Wrap function which
    Start function editor() for edition without validation.
    """
    editor(mode='edit', validation_mod=validation_mod)


def remove_(validation_mod=False):
    """
    Wrap function which
    Start function editor() for remove without validation.
    """
    editor(mode='remove', validation_mod=validation_mod)
