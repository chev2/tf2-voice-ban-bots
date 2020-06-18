import json #json parse
import os #path/file opening
import re #regex
import requests #http requests

tf2_playerlist_url = "https://raw.githubusercontent.com/PazerOP/tf2_bot_detector/master/staging/cfg/playerlist.official.json" #Pazer's list of bots
tf2_playerlist_url_2 = "https://raw.githubusercontent.com/chev2/tf2-voice-ban-bots/master/voice_ban_users.json" #My list of bots
github_headers = {
    'User-Agent': 'tf2-voice-ban-bots/1.0 (Python script - written by github.com/chev2)'
}
steamid3_regex = r'(\[U:1:\d+\])'
cwd = os.getcwd()
players = []

print("Attempting connection to bots list...")


#Pazer's bot list
r = requests.get(tf2_playerlist_url, headers=github_headers)

if r.status_code != 200:
    print(f"HTTP Error {r.status_code} to Pazer's bot list has occured.")
else:
    print("Connection to Pazer's bot list successful.")

json_info = r.json()

for player in json_info["players"]:
    players.append(player["steamid"])

print("{0} bots found in Pazer's list.".format(len(players)))


#My bot list
r = requests.get(tf2_playerlist_url_2, headers=github_headers)

if r.status_code != 200:
    print(f"HTTP Error {r.status_code} to Chev's bot list has occured.")
else:
    print("Connection to Chev's bot list successful.")

json_info = r.json()

for player in json_info:
    players.append(player)

print("{0} bots found in Chev's list.".format(len(json_info)))

print("{0} bots found in total.".format(len(players)))

mergefilequery = None
path = None
mergeplayers = []

while mergefilequery not in ("y", "n"):
    mergefilequery = input("Would you like to merge your current voice_ban.dt file with the bots list? [y/n]: ")
    if mergefilequery.lower() == "y":
        while True:
            path = input("Please specify the file path to your voice_ban.dt file: ")
            if os.path.isfile(path):
                break

        with open(path, "r") as mergefile:
            filestr = mergefile.read()
            for player in re.finditer(steamid3_regex, filestr):
                mergeplayers.append(player.group(1))

        print("Found {0} players in the provided file, adding them to the final muted players list.".format(len(mergeplayers)))

        players += mergeplayers #add the user-provided mutes to the grabbed player mutes
    elif mergefilequery.lower() == "n":
        print("Skipping merge step...")

dupe_number = len(players) - len(set(players)) #get number of duplicates
players = set(players) #remove duplicates in case of merging

players_as_string = "\x01\0\0\0" + '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'.join(players) + '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0' #this is how the voice_ban.dt file is patterned

print("{0} muted players in total. Removed {1} duplicates.".format(len(players), dupe_number))

writetofile = None

while writetofile not in ("y", "n"):
    writetofile = input("Write the muted bots to a new voice_ban.dt file? [y/n]: ")
    if writetofile.lower() == "y":
        with open("voice_ban.dt", "w") as file: #write muted players
            file.seek(0) #go to beginning of the file
            file.write(players_as_string) #write muted players
            file.truncate()

        print("Wrote players to {0}\\voice_ban.dt".format(cwd))
    elif writetofile.lower() == "n":
        print("Exitting...")
