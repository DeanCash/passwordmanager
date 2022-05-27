import os
import sys
import json
import base64
import subprocess
from socket import gethostname
from colorama import Fore, Style;

reset_color = Fore.RESET
current_program = sys.argv[0]
current_user = os.getenv("USERNAME")
pc_name      = gethostname()
rootfolder   = "DeansPasswordManager"
roamingpath  = f"C:\\Users\\{current_user}\\AppData\\Roaming"
rootpath     = os.path.join(roamingpath, rootfolder)
json_file_name = "pw_storage.json"
json_backup_file_name = "pw_storage_BACKUP.json"
full_json_path = os.path.join(rootpath, json_file_name)
full_backup_json_path = os.path.join(rootpath, json_backup_file_name)

prefix = {
    "error": f"{Fore.LIGHTRED_EX} :  ",
    "warning": f"{Fore.LIGHTYELLOW_EX} :  ",
    "success": f"{Fore.LIGHTGREEN_EX} :  ",
    "log": f"{Fore.LIGHTCYAN_EX} :  ",
    "purple": f"{Fore.LIGHTMAGENTA_EX} :  ",
    "reset": f"{Fore.RESET}{Style.RESET_ALL}"
}

# add a Path to global 'Path' ENV variables
def add_path_env_var(path_to_add: str) -> None:
    # if path already in 'Path' ENV variables, then return
    if path_to_add in os.environ["Path"]:
        return
    os.system(f'setx PATH "{path_to_add};%PATH%" >nul 2>&1')

# remove a Path to global 'Path' ENV variables
def remove_path_env_var(path_to_remove: str) -> None:
    # if path not in 'Path' ENV variables, then return
    if not (path_to_remove in os.environ["Path"]):
        return
    new_path_env = os.environ["Path"].replace(f"{path_to_remove};", "")
    new_path_env = os.environ["Path"].replace(f"{path_to_remove}", "")
    os.system(f'setx PATH "{new_path_env}" >nul 2>&1')

# error message if invalid command on command line
def usage_error(abort: bool = False, no_args_error: bool = True) -> None:
    if no_args_error: print(" No Arguments Passed")
    print(" USAGE:  pm [args]")
    print("   [args]:")
    print("    - changemp [master password]")
    print("    - create (new password)")
    print("    - remove (index)")
    print("    - copy (index)")
    print("    - listpw")
    if abort: sys.exit(1)

# error message if there is something wrong
# with the storage directory
def storage_error(abort: bool = False) -> None:
    print(" There is something wrong with the storage directory")
    print(" ... perhaps try running the uninstaller")
    print(" ... and then the installer again")
    if abort: sys.exit(1)

# error message if inputted password is not the master password
def mp_error(abort: bool = False) -> None:
    print(f" Invalid master password - try again.")
    if abort: sys.exit(1)

# encrypt a string
def encrypt(password: str) -> str:
    # swap dictionary
    encoding_list = {
        "s": "qpl",
        "a": "mnb",
        "e": "ytr",
        "u": "hjk",
        "1": "45",
        "h": "v3"
    }
    # swap all letters with random values
    encrypted_password = base64.b64encode(bytes(password, "UTF-8")).decode("UTF-8")
    for encode_key, encode_value in encoding_list.items():
        encrypted_password = encrypted_password.replace(encode_key, encode_value)
    return f"%{encrypted_password}%"

# decrypt a string
def decrypt(encrypted_string: str) -> str:
    # remove dummy characters %
    encrypted_string = encrypted_string.replace("%", "")
    # reversed swap dictionary
    decoding_list = {
        "v3": "h",
        "45": "1",
        "hjk": "u",
        "ytr": "e",
        "mnb": "a",
        "qpl": "s"
    }
    # swap all original characters back to original
    for encode_key, encode_value in decoding_list.items():
        encrypted_string = encrypted_string.replace(encode_key, encode_value)
    try: decrypted_password = base64.b64decode(bytes(encrypted_string, "UTF-8")).decode("UTF-8")
    except: return encrypted_string
    return decrypted_password

# check if the JSON is not like its supposed to / missing any default keys
# return True if damaged: missing path, or missing key in JSON
def is_json_damaged(json_path: str) -> bool:
    check_for = [
        "master_password",
        "encrypted_passwords"
    ]
    try:
        with open(json_path, "r") as f: content = json.load(f)
        for item in check_for:
            if not (item in content.keys()): return True
        return False
    except: return True

# create save json folder if not exists
def create_storage_json(root_folder: str) -> None:
    default_json_layout = {
        "master_password": "NULLVALUE",
        "encrypted_passwords": []
    }
    
    # if storage json already exists, copy contents and put in backup file, then overwrite
    # with default contents since setup is ran again
    if os.path.exists(full_json_path):
        if is_json_damaged(full_json_path):
            with open(full_json_path, "w+") as f: json.dump(default_json_layout, f, indent=4)
        else:
            try:
                with open(full_json_path, "r") as f: backupdata = json.load(f)
            except: storage_error(True)
            with open(full_backup_json_path, "w+") as f: json.dump(backupdata, f, indent=4)
    
    # write default contents to storage json
    with open(full_json_path, "w+") as f:
        json.dump(default_json_layout, f, indent=4)

# create save JSON folder if not exists
def check_master_password_exists(json_path: str) -> bool:
    if is_json_damaged(full_json_path): storage_error(True)
    with open(json_path, "r") as f: content = json.load(f)
    if content['master_password'] == "NULLVALUE":
        return False
    return True

# set new master password in JSON
def set_new_master_password(json_path: str, new_password: str) -> None:
    with open(json_path, "r") as f: content = json.load(f)
    with open(json_path, "w+") as f:
        content['master_password'] = encrypt(new_password)
        json.dump(content, f, indent=4)

# check if inputted password is the master password
def check_if_master_password(json_path: str, inputted_password: str) -> bool:
    with open(json_path, "r") as f: content = json.load(f)
    actual_master_password = decrypt(content['master_password'])
    if (inputted_password == actual_master_password):
        return True
    return False

# returns amount of values inside of a list in a JSON key
def get_amount_of_items_json_list(json_path: str, sub_obj: str) -> int:
    with open(json_path, "r") as f:
        for i, _ in enumerate(json.load(f)[sub_obj], 1):
            count = i
    return count

# encrypt a password and add it to save json
def encrypt_and_add_to_json_list(json_path: str, sub_obj: str, password: str) -> None:
    if is_json_damaged(full_json_path): storage_error(True)
    encrypted_password = encrypt(password)
    with open(json_path, "r") as f: contents = json.load(f)
    with open(json_path, "w+") as f:
        contents[sub_obj].append(encrypted_password)
        json.dump(contents, f, indent=4)

# return list of all passwords (decrypted)
def get_and_decrypt_all_from_list(json_path: str, sub_obj: str) -> list[str]:
    if is_json_damaged(full_json_path): storage_error(True)
    with open(json_path, "r") as f: content = json.load(f)
    pw_lst = []
    for item in content[sub_obj]:
        try: pw_lst.append(decrypt(item))
        except: pw_lst.append(item)
    return pw_lst

# return single decrypted passwords of choice from storage JSON
def get_and_decrypt_password(json_path: str, sub_obj: str, num_choice: int, json_check: bool = True) -> str:
    num_choice -= 1
    if json_check:
        if is_json_damaged(json_path): storage_error(True)
    with open(json_path, "r") as f: content = json.load(f)
    password_list = content[sub_obj]
    specified_password = password_list[num_choice]
    return decrypt(specified_password)

# remove a password from the storage JSON
def remove_single_password(json_path: str, sub_obj: str, num_choice: int, json_check: bool = True) -> str:
    num_choice -= 1
    if json_check:
        if is_json_damaged(json_path): storage_error(True)
    with open(json_path, "r") as f: content = json.load(f)
    deleted_password = content[sub_obj].pop(num_choice)
    with open(json_path, "w+") as f:
        json.dump(content, f, indent=4)
    return decrypt(deleted_password)

# copies a string to your clipboard
def copy_to_clipboard(string: str) -> str:
    cmd='echo '+string.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)



# debugging and testing purposes
if __name__ == "__main__":
    print(get_and_decrypt_password("save.json", "e", 1, json_check=False))