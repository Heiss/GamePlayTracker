import subprocess
import json
from time import time

class ProcessSearcher():
    executable_list = []
    known_games = None
    playtime = None

    def __init__(self):
        with open('data/games.json') as data_file:    
            self.known_games = json.load(data_file)
        
        with open('data/playtime.json') as data_file:    
            self.playtime = json.load(data_file)

    def read_process(self):
        cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        for line in proc.stdout:
            try:
                self.executable_list.append(line.decode().split()[0])     
            except IndexError as err:
                pass

        # remove duplicates
        self.executable_list = list(set(self.executable_list))

    def print_process(self):
        print(self.executable_list)

    def loop(self):
        self.read_process()
        self.search_for_known_exe()

        print(self.playtime)
        
        self.save_playtime()

    def search_for_known_exe(self):
        for line in self.executable_list:
            try:
                index = self.known_games[line]
                self.add_playtime(line)
            except KeyError as err:
                pass
    
    def add_playtime(self, game):
        # already played?
        if game in self.playtime:
            self.playtime[game]["last_played"] = int(time())
            self.playtime[game]["playtime_seconds"] = self.playtime[game]["playtime_seconds"] + 1
        # not played before
        else:
            gameplay = {    "last_played": int(time()),
                            "playtime_seconds": 1,
                            "first_played": int(time())
                        }
            self.playtime.update({game: gameplay})

    def save_playtime(self):
        with open('data/playtime.json', 'w') as outfile:
            json.dump(self.playtime, outfile)