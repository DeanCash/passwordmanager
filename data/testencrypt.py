import os; os.system("cls")
import sys
import time
import json
import base64
import colorama; colorama.init(autoreset=True)
from colorama import Fore

json_file = os.path.join(os.getcwd(), "save.json")
loop_amount = 25

def enc(string: str) -> str:
    dict = {
        "a": "ma/",
        "e": "a1",
        "i": "skai",
        "h": "0s;1",
        "s": "w91",
        "d": "02;",
        "u": "20*",
        "o": "was@ds",
        " ": "aps"
    }
    string = base64.b64encode(bytes(string, "UTF-8")).decode("UTF-8")
    amount = loop_amount
    for _ in range(amount):
        for key, value in dict.items():
            string = string.replace(key, value)
    return string

def dec(enc_string: str) -> str:
    dict = {
        "aps": " ",
        "was@ds": "o",
        "20*": "u",
        "02;": "d",
        "w91": "s",
        "0s;1": "h",
        "skai": "i",
        "a1": "e",
        "ma/": "a"
    }
    amount = loop_amount
    for _ in range(amount):
        for key, value in dict.items():
            enc_string = enc_string.replace(key, value)
    return enc_string

if __name__ == "__main__":
    str1 = "hallo mijn naam is dean"
    print(str1, "\n")
    time.sleep(1.5)
    print(enc(str1), "\n")
    time.sleep(1.5)
    print(dec(str1))

    # os.system("pause>nul")