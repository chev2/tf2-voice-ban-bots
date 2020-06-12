import os
import json
import requests

tf2_playerlist_url = "https://raw.githubusercontent.com/PazerOP/tf2_bot_detector/master/tf2_bot_detector/cfg/playerlist.official.json" #Pazer's list of bots
github_headers = {
    'User-Agent': 'tf2-voice-ban-bots/1.0 (Python script - written by github.com/chev2)'
}
cwd = os.getcwd()

print("Attempting connection to bots list...")

r = requests.get(tf2_playerlist_url, headers=github_headers)

if r.status_code != 200:
    print("HTTP Error {0} has occured".format(r.status_code))
else:
    print("Connection successful")

json_info = json.loads(r.content)

players = []
for player in json_info["players"]:
    players.append(player["steamid"])

print("{0} bots found in json".format(len(players)))

players_as_string = "\x01\0\0\0" + '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0'.join(players) + '\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0' #this is how the voice_ban.dt file is patterned

writetofile = ""

def AskToWriteFile():
    global writetofile
    writetofile = input("List of players has been successfully found. Write the muted bots to a new voice_ban.dt file? [y/n]: ")

AskToWriteFile()

if writetofile.lower() == "y": #create the file if the user says yes
    with open("voice_ban.dt", "w") as file: #write muted players
        file.seek(0) #go to beginning of the file
        file.write(players_as_string) #write muted players
        file.truncate()

    print("Wrote players to {0}\\voice_ban.dt".format(cwd))
elif writetofile.lower() == "n": #exit the program if the user says no
    print("Exitting...")
else:
    AskToWriteFile()
