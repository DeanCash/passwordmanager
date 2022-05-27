import sys
import getpass
from resc import *

# if no arguments passed
if len(sys.argv) <= 1:
    # if there is no master password configured yet
    if not (check_master_password_exists(full_json_path)):
        print(f"\n Welcome to PasswordManager, no master password has been")
        print(f" ... configured yet - please do that here! >> ", end=""); master_password = input().strip()
        print(f"\n Confirm [Y/N] > ", end=""); confirm_mp = input().lower().strip()
        if (confirm_mp == "y") or (confirm_mp == "yes") or (confirm_mp == "confirm"):
            set_new_master_password(full_json_path, master_password)
            print(f" Master password has successfully been set!")
        else:
            print(f" Master password has not been set.")
        sys.exit(0)
    usage_error(True)

# if 1 argument has been passed
if len(sys.argv) == 2:
    #? if help arg
    if (sys.argv[1].lower() == "help") or (sys.argv[1].lower() == "?") or (sys.argv[1].lower() == "/?"):
        usage_error(False, False)
        sys.exit(0)
    #? if listpasswords arg
    elif sys.argv[1] == "listpw":
        mp_check = getpass.getpass(" password: ");
        if not (check_if_master_password(full_json_path, mp_check)):
            mp_error(True)
        passwords = get_and_decrypt_all_from_list(full_json_path, "encrypted_passwords")
        for i, password in enumerate(passwords, 1):
            print(f" {i}: {password}")
    #? if changemasterpassword arg
    elif sys.argv[1] == "changemp":
        mp_check = getpass.getpass(" password: ");
        if not (check_if_master_password(full_json_path, mp_check)):
            mp_error(True)
        print(f" Set new master password > ", end=""); new_master_password = input().strip()
        set_new_master_password(full_json_path, new_master_password)
        print(f"\n New master password has been set!")
    else: usage_error(True)
    sys.exit(0)

# if 2 arguments have been passed
elif len(sys.argv) == 3:
    #? if create arg
    if sys.argv[1].lower() == "create":
        mp_check = getpass.getpass(" password: ");
        if not (check_if_master_password(full_json_path, mp_check)):
            mp_error(True)
        # check if password doesn't already exist
        passwords = get_and_decrypt_all_from_list(full_json_path, "encrypted_passwords")
        for password in passwords:
            if sys.argv[2] == password:
                print(f"\n This password already exists - you can't store")
                print(f" ... the same password more than once")
                sys.exit(1)
        # if not already exist add to JSON
        encrypt_and_add_to_json_list(full_json_path, "encrypted_passwords", sys.argv[2])
        print(f" Added : {sys.argv[2]} : to stored passwords")
        sys.exit(0)
    #? if copy arg
    if sys.argv[1].lower() == "copy":
        mp_check = getpass.getpass(" password: ");
        if not (check_if_master_password(full_json_path, mp_check)):
            mp_error(True)
        try: number_choice = int(sys.argv[2])
        except:
            print(f"\n Choice must be a valid number key from password list")
            print(f" ... try again with an existing number choice")
            sys.exit(1)
        amount_passwords = get_amount_of_items_json_list(full_json_path, "encrypted_passwords")
        # check if inputted value is a number, and if falls in range
        if (number_choice >= 1) and (number_choice <= amount_passwords):
            selected_password = get_and_decrypt_password(full_json_path, "encrypted_passwords", number_choice)
            succeeded = copy_to_clipboard(selected_password)
            if not (succeeded == 0):
                print(f"\n Copying to clipboard failed unexpectedly")
                print(f" ... perhaps try again\n")
            else:
                print(f"\n Password : {selected_password} : copied to clipboard\n")
                sys.exit(0)
        else:
            print(f"\n Choice must be a valid number key from password list")
            print(f" ... try again with an existing number choice")
            sys.exit(1)
    #? if remove arg
    if sys.argv[1].lower() == "remove":
        mp_check = getpass.getpass(" password: ");
        if not (check_if_master_password(full_json_path, mp_check)):
            mp_error(True)
        try: remove_choice = int(sys.argv[2])
        except:
            print(f"\n Choice must be a valid number key from password list")
            print(f" ... try again with an existing number choice")
            sys.exit(1)
        amount_passwords = get_amount_of_items_json_list(full_json_path, "encrypted_passwords")
        # check if inputted value is a number, and if falls in range
        if (remove_choice >= 1) and (remove_choice <= amount_passwords):
            removed_password = remove_single_password(full_json_path, "encrypted_passwords", remove_choice)
            print(f"\n Successfully removed : {removed_password} : from saved passwords\n")
        else:
            print(f"\n Choice must be a valid number key from password list")
            print(f" ... try again with an existing number choice")
            sys.exit(1)
    else: usage_error(True)
    sys.exit(0)

# if any anvalid command specify what goes wrong
else:
    # if too many arguments given to create command
    if sys.argv[1].lower() == "create":
        print(" You can't have spaces in a password")
        print(" ... try again without whitespaces\n")
        sys.exit(1)
    # if too many arguments given to remove command
    if sys.argv[1].lower() == "remove":
        print(" You can't have spaces in a password")
        print(" ... try again without whitespaces\n")
        sys.exit(1)
    # if too many arguments given to copy command
    if sys.argv[1].lower() == "copy":
        print(" Choose a number")
        print(" ... try again without whitespaces\n")
        sys.exit(1)
    print(" Not a valid command - use 'pm help'")
    print(" ... for help with commands\n")
    sys.exit(1)