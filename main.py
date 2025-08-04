from replit import db
import datetime, os, time, random
import hashlib

fileExists = True
try:
  f = open("Diary.txt", "r")
  diary = eval(f.read())
  f.close()
except Exception as err:
  fileExists = False
  diary = []

def hash_password(password, salt):
    return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

def addEntry():
    global diary
    os.system("clear")
    timestamp = datetime.datetime.now().isoformat()
    print(f"Diary entry for {timestamp}\n")
    entry = input("> ")
    both = f"{entry} at {timestamp}"
    diary.append(both)
    db[f"{username}:{timestamp}"] = entry
    print("Entry saved!")

def viewEntry():
    entries = [key for key in db.keys() if key.startswith(f"{username}:")]
    entries.sort()
    for key in entries:
        os.system("clear")
        print(f"{key.split(':')[1]}\n{db[key]}\n")
        opt = input("Next or exit? > ")
        if opt.lower().startswith("e"):
            break

# Account setup or login
os.system("clear")
keys = db.keys()

if "users" not in db:
    db["users"] = {}

if not db["users"]:
    print("First Run > Create account")
    username = input("Username > ")
    password = input("Password > ")
    salt = str(random.randint(0, 9999999))
    hashed = hash_password(password, salt)
    db["users"][username] = {"password": hashed, "salt": salt}
else:
    print("Log in")
    username = input("Username > ")
    password = input("Password > ")

    if username not in db["users"]:
        print("Username or password incorrect")
        exit()

    salt = db["users"][username]["salt"]
    hashed = hash_password(password, salt)

    if db["users"][username]["password"] != hashed:
        print("Username or password incorrect")
        exit()

# Diary menu
diary = []
while True:
    os.system("clear")
    menu = input("1: Add\n2: View\n3: Exit\n> ").strip()
    if menu == "1":
        addEntry()
    elif menu == "2":
        viewEntry()
    elif menu == "3":
        print("Bye!")
        break
    else:
        print("Invalid choice.")
        
    f = open("Diary.txt", "w")
    f.write(str(diary))
    f.close()
