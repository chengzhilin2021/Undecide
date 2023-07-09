#!/usr/bin/python3
# coding=utf-8

import base64
import hashlib
import json
import os
import requests
import time


def save(path, mode):
    tojson = json.dumps(path)
    savejson = open('./.config/' + mode + '.json', 'w')  # setups/datas
    savejson.write(tojson)
    savejson.close()


errornum = 0

if not os.path.exists("./.config"):
    os.makedirs("./.config")

if not os.path.exists("./.config/setups.json"):
    savedefault = open('./.config/setups.json', 'w')

if not os.path.exists("./.config/datas.json"):
    savedefault = open('./.config/datas.json', 'w')

if os.path.getsize('./.config/setups.json') == 0:
    setup = {'version': "Error!"}
else:
    with open("./.config/setups.json", 'rb') as f:
        params = json.load(f)
        setup = params
        if 'version' not in setup.keys():
            setup['version'] = "Error!"

if os.path.getsize('./.config/datas.json') == 0:
    data = {}
else:
    with open("./.config/datas.json", 'rb') as f:
        params = json.load(f)
        data = params

print("Welcome to the database beta version:" + str(setup['version']) + "\nPlease enter commands")
if 'username' not in setup or len(setup['username']) == 0:
    print("Now,sign up for your account")
    while True:
        username = input("your name:")
        if username == 'update':
            with open('./update.py') as f:
                exec(f.read())
            quit()
        userpasswd = input("your password:")
        if len(username) == 0 or len(userpasswd) == 0 or username == 'update':
            print("Your input is incorrect, please re-enter it")
            continue
        else:
            break
    userpasswd1 = hashlib.md5()
    userpasswd1.update(userpasswd.encode())
    setup['username'] = username
    setup['userpasswd'] = userpasswd1.hexdigest()
    save(setup, 'setups')
else:
    while True:
        if errornum >= 3:
            while True:
                select = input("Whether to reset the password?yes/no")
                if select == "yes":
                    while True:
                        username = input("original username:")
                        if username != setup['username']:
                            print("Your input is incorrect, please re-enter it")
                            continue
                        userpasswd = input("your password:")
                        if len(username) == 0 or userpasswd == 0:
                            print("Your input is incorrect, please re-enter it")
                            userpasswd1 = hashlib.md5()
                            userpasswd1.update(userpasswd.encode())
                            setup['username'] = username
                            setup['userpasswd'] = userpasswd1.hexdigest()
                            continue
                        else:
                            break
                    break
                elif select == "no":
                    errornum = 0
                    break
                else:
                    print("Your input is incorrect, please re-enter it")
                    continue
        username = input("your username:")
        if username == 'update':
            with open('./update.py') as f:
                exec(f.read())
            quit()
        userpasswd = input("your password:")
        userpasswd1 = hashlib.md5()
        userpasswd1.update(userpasswd.encode())
        if username == setup["username"] and userpasswd1.hexdigest() == setup["userpasswd"]:
            print("Enter correctly")
            errornum = 0
            break
        else:
            print("Your input is incorrect, please re-enter it")
            errornum += 1
            continue
while True:
    command = str(input("Command>>"))
    if command == 'exit':
        print("Bye!")
        quit()
    elif command == "add":
        key = input("Please enter key:")
        value = input("Please enter value:")
        encrypt = base64.b64encode(value.encode()).decode('utf-8')
        data[key] = str(encrypt)
        save(data, 'datas')
        print("Completed")
    elif command == 'search':
        key = input("Please enter the key:")
        if key in data.keys():
            print("Search successful!")
            value = data[key].encode()
            out = base64.b64decode(value)
            print(out.decode())
    elif command == "help":
        print("'exit' -> exit | 'help' -> help\n'add' -> add value | 'search' -> input key search value")
    else:
        print("The command entered is incorrect")
