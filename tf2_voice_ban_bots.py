import json #json parse
import os #path/file opening
import re #regex
import requests #http requests

tf2_botlist_urls = {
    "Pazer": "https://raw.githubusercontent.com/PazerOP/tf2_bot_detector/master/staging/cfg/playerlist.official.json", #Pazer's list of bots
    "Chev": "https://raw.githubusercontent.com/chev2/tf2-voice-ban-bots/master/voice_ban_users.json", #My list of bots
    "wgetJane": "https://gist.githubusercontent.com/wgetJane/0bc01bd46d7695362253c5a2fa49f2e9/raw/fefb98e0e10bbab8ff1b38e96adbaabf4a8db94f/bot_list.txt" #wgetJane's list of bots
}
github_headers = {
    'User-Agent': 'tf2-voice-ban-bots/1.0 (Python script - written by github.com/chev2)'
}

steamID64IDEnt = 76561197960265728
steamIDlen = 32

steamid3_regex = r'(\[U:1:\d+\])'
wgetjane_list_regex = r'\n(\d+)'

cwd = os.getcwd()
players = []

def SteamID64To3(id):
    id3base = int(id) - steamID64IDEnt
    return "[U:1:{0}]".format(id3base)

print("Attempting connection to bots list...")
for url in tf2_botlist_urls:
    cur_players = []

    print(f"Attempting connection to {url}'s bot list...")
    r = requests.get(tf2_botlist_urls[url], headers=github_headers)
    if r.status_code != 200:
        print(f"HTTP Error {r.status_code} to {url}'s list has occurred.")
    else:
        print(f"Connection to bot {url}'s bot list successful.")

    if url == "Pazer":
        js = r.json()

        for player in js["players"]:
            cur_players.append(player["steamid"])

        players += cur_players
    elif url == "Chev":
        js = r.json()

        for player in js:
            cur_players.append(player)
        players += cur_players
    elif url == "wgetJane":
        txt = r.content

        for player64 in re.finditer(wgetjane_list_regex, txt.decode('UTF-8')):
            player = SteamID64To3(player64.group(1))
            cur_players.append(player)

        players += cur_players

    print(f"{format(len(cur_players), ',d')} bots found in {url}'s list.")

players = list(set(players)) #remove duplicates in case there are multiple of the same ID in any list

print(f"{format(len(players), ',d')} bots found in total.")

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
players = sorted(set(players), key=lambda x: len(x)) #remove duplicates in case of merging, also sort by ID length (the voice_ban.dt file will break if not sorted)

for player in range(0, len(players)):
    players[player] += "\0"*(steamIDlen-len(players[player])) #steam ID length plus whitespace should always equal 32 characters

players_as_string = "\x01\0\0\0" + ''.join(players) #this is how the voice_ban.dt file is patterned

print(f"{format(len(players), ',d')} muted players in total. Removed {dupe_number} duplicates.")

writetofile = None

while writetofile not in ("y", "n"):
    writetofile = input("Write the muted bots to a new voice_ban.dt file? [y/n]: ")
    if writetofile.lower() == "y":
        with open("voice_ban.dt", "wb") as file: #write muted players
            file.seek(0) #go to beginning of the file
            file.write(str.encode(players_as_string)) #write muted players
            file.truncate()

        print("Wrote players to {0}\\voice_ban.dt".format(cwd))
    elif writetofile.lower() == "n":
        print("Exitting...")
