import os
import sys
import ctypes
os.system("TITLE PMinstaller - by D.")

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

import colorama
colorama.init(autoreset=True)
if not isAdmin():
    print(f"\n {colorama.Fore.LIGHTRED_EX}:  {colorama.Fore.LIGHTBLUE_EX}Please run the installer again, but with admin permissions")
    print(f" {colorama.Fore.LIGHTWHITE_EX}   ... {colorama.Fore.LIGHTBLUE_EX}to ensure nothing goes wrong in the installation{colorama.Fore.RESET}\n")
    print(f" Press any key to close: ", end="")
    os.system("pause>nul")
    sys.exit(0)

import time
import shutil
import requests
import threading
from socket import gethostname
from resc import prefix, add_path_env_var, remove_path_env_var, create_storage_json

current_program = sys.argv[0]
current_user = os.getenv("USERNAME")
pc_name      = gethostname()
rootfolder   = "DeansPasswordManager"
roamingpath  = f"C:\\Users\\{current_user}\\AppData\\Roaming"
rootpath     = os.path.join(roamingpath, rootfolder)
pm_exe       = os.path.join(rootpath, "pm.exe")
URL = r"https://download1320.mediafire.com/r8urh31u85ng/1jbj33xbquqyi08/PM.exe"

print()
# if rootfolder and/or path ENV variables already exist, delete them
if os.path.exists(rootpath):
    try:
        shutil.rmtree(rootpath)
        print(f"{prefix['warning']}PasswordManager root directory already exists - so deleted{prefix['reset']}")
    except: pass
# if ((f"{rootpath};") in os.environ["Path"]):
#     new_path_env = os.environ["Path"].replace(f"{rootpath};", "")
#     os.system(f'setx PATH "{new_path_env}" >nul 2>&1')
#     print(f"\n{prefix['warning']}Global enviroment path variable already exists - so deleted{prefix['reset']}")
if ((f"{rootpath}") in os.environ["Path"]):
    remove_path_env_var(rootpath)
    print(f"{prefix['warning']}Global enviroment path variable already exists - so deleted{prefix['reset']}")
# - - - - - - - - - - #

response: requests.Response
def get_response():
    global response
    response = requests.get(URL, allow_redirects=True)
get_response_thread = threading.Thread(target=get_response, daemon=True)

try:
    # retrieve/download .exe contents from internet
    count = 0
    load_lst = ["o..", ".o.", "..o", "..."]
    
    if not (os.path.exists(pm_exe)):
        get_response_thread.start()
        while True:
            if count == len(load_lst):
                count = 0
            if threading.active_count() == 1:
                break
            print(f"{prefix['log']}Downloading PasswordManager  {load_lst[count]}{prefix['reset']}", end="\r")
            count += 1
            time.sleep(0.3)
        print(f"{prefix['log']}Downloading PasswordManager  DONE{prefix['reset']}")
        print(f"{prefix['log']}Finished downloading PasswordManager{prefix['reset']}")

    # create the PasswordManager/(root) directory in the Roaming folder
    print(f"{prefix['log']}Creating root save directory in -> {roamingpath}{prefix['reset']}")
    if not os.path.exists(rootpath):
        os.mkdir(rootpath)
    print(f"{prefix['log']}Finished creating -> {rootpath}{prefix['reset']}")

    # creating the PM.exe inside the root folder
    print(f"{prefix['log']}Initializing PasswordManager PM{prefix['reset']}")
    with open(os.path.join(rootpath, pm_exe), "wb+") as f:
        f.write(response.content)

    print(f"{prefix['log']}Creating password storage environment...{prefix['reset']}")
    print(f"{prefix['log']}Creating json password storage{prefix['reset']}")
    create_storage_json(rootpath)
    
    # add the root folder to global Path ENV so PM becomes accessible globally in CMD
    print(f"{prefix['log']}Adding PM to global path environment variables{prefix['reset']}")
    add_path_env_var(rootpath)

    # delete itself/(PMinstaller.py) from pc
    #! os.remove(current_program)
    
    print(f"\n{prefix['success']}Successful installation! You can go can now use PM inside of your{prefix['reset']}")
    print(f"{colorama.Fore.LIGHTGREEN_EX}    ... standard windows CMD, by just typing 'pm'{prefix['reset']}")
    
    print(f" Press any key to close: ", end="")
    os.system("pause>nul")

except:
    print(f"\n{prefix['error']}Something unexpected went wrong :( ", end="")
    os.system("pause>nul")
    sys.exit(1)

sys.exit(0)