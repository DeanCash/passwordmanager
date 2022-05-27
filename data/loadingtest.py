from resc import prefix
import time, threading
def test():
    count = 0
    for i in range(100000000):
        count += 1
get_response_thread = threading.Thread(target=test)

count = 0
load_lst = ["o..", ".o.", "..o", "..."]
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