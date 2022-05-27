import os
import sys
import ctypes
from resc import prefix, remove_path_env_var
os.system("TITLE PMuninstaller - by D.")

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

import colorama
colorama.init(autoreset=True)
if not isAdmin():
    print(f"\n {colorama.Fore.LIGHTRED_EX}:  {colorama.Fore.LIGHTBLUE_EX}Please run the uninstaller with administrator permissions")
    print(f" {colorama.Fore.LIGHTWHITE_EX}   ... {colorama.Fore.LIGHTBLUE_EX}to ensure everything gets cleaned up {colorama.Fore.LIGHTWHITE_EX}:){colorama.Fore.RESET}\n")
    print(f" Press any key to close: ", end="")
    os.system("pause>nul")
    sys.exit(0)

import shutil
from socket import gethostname

current_program = sys.argv[0]
current_user = os.getenv("USERNAME")
pc_name      = gethostname()
rootfolder   = "DeansPasswordManager"
roamingpath  = f"C:\\Users\\{current_user}\\AppData\\Roaming"
rootpath     = os.path.join(roamingpath, rootfolder)

not_found = False
file_delete_count = 1

print()
# uninstall / remove everything that is installed of PasswordManager
if os.path.exists(rootpath):
    print(f"{prefix['success']}Started uninstall process...{prefix['reset']}")
    for path, folders, files in os.walk(rootfolder):
        for file in files:
            current_file = os.path.join(path, file)
            if os.path.isfile(current_file):
                try:
                    os.remove(current_file)
                    print(f"\n{prefix['log']}Deleted {file_delete_count}: {file}{prefix['reset']}")
                except: pass
    print(f"{prefix['log']}Successfully deleted all storage files{prefix['reset']}")
else:
    not_found = True

# delete entire root directory tree
if os.path.exists(rootpath):
    try:
        shutil.rmtree(rootpath)
        print(f"{prefix['log']}Successfully removed entire root directory tree{prefix['reset']}")
    except: pass
else:
    not_found = True

# if root directory not found display warning message
if not_found:
    print(f"\n{prefix['warning']}{rootfolder}Root storage folder can not be found, or is already deleted!{prefix['reset']}")

# remove itself from Path ENV variables
remove_path_env_var(rootpath)
print(f"{prefix['log']}Successfully removed from global Path Environment Variables{prefix['reset']}")

print(f"{prefix['success']}SUCCESS: Uninstallation completed{prefix['reset']}")
print(f" Press any key to close: ", end="")
os.system("pause>nul")
sys.exit(0)