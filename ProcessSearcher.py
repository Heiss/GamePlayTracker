import subprocess
import json
from time import time, strftime, gmtime, sleep
import threading


class ProcessSearcher(threading.Thread):
    executable_list = []
    known_games = None
    playtime = None
    current_game = None
    current_game_started = time()
    isRunning = False
    label_playtime = None

    def __init__(self):
        threading.Thread.__init__(self)

        self.isRunning = False

        with open('data/games.json') as data_file:
            self.known_games = json.load(data_file)

        with open('data/playtime.json') as data_file:
            self.playtime = json.load(data_file)

    def run(self):
        self.isRunning = True

        while self.isRunning:
            self.change_label_text()
            self.loop()
            sleep(0.8)

        # save the files for security and shutdown
        self.store_playtime_to_file()

    def get_running_status(self):
        return self.isRunning

    def stop_loop(self):
        self.isRunning = False

    def read_process_manager(self):
        # empty list
        self.executable_list = []

        cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        for line in proc.stdout:
            try:
                self.executable_list.append(line.decode().split()[0])
            except IndexError as err:
                pass

        # remove duplicates
        self.executable_list = list(set(self.executable_list))

    def set_label(self, label):
        self.label_playtime = label

    def change_label_text(self):
        if self.current_game in self.known_games:
            game = self.known_games[self.current_game]["title"]
        else:
            game = "None"
        self.label_playtime[
            "text"] = "Currently playing (Time): {} ({})".format(
                game,
                strftime("%H:%M:%S",
                         gmtime(time() - self.current_game_started)))

    def get_current_game(self):
        return self.current_game, self.current_game_started

    def get_tracked_games(self):
        return self.known_games

    def print_process(self):
        print(self.executable_list)

    def loop(self):
        #first identify all running processes
        self.read_process_manager()

        # find the game, which is currently running
        if self.current_game is None:
            self.current_game = self.search_for_trackable_exe()

            # no game found? abort
            if self.current_game is None:
                print("{}: No game found.".format(time()))
                return

            self.current_game_started = time()

        # is the game currently running?
        elif self.current_game in self.executable_list:
            print("{}: {} is currently playing.".format(
                time(), self.current_game))

        # game is not running anymore
        else:
            # calculate the running time
            time_running = int(time() - self.current_game_started)

            # game was playing before
            if self.current_game in self.playtime:
                # add the time to the datastructure
                self.playtime[self.current_game]["last_played"] = int(time())
                self.playtime[self.current_game][
                    "playtime_seconds"] = self.playtime[self.
                                                        current_game]["playtime_seconds"] + time_running
            # game was not playing before
            else:
                gameplay = {
                    "last_played": int(time()),
                    "playtime_seconds": time_running,
                    "first_start": int(self.current_game_started)
                }
                self.playtime.update({self.current_game: gameplay})

            # reset current game and time
            self.current_game = None
            self.current_game_started = time()

            # save the data in file
            self.store_playtime_to_file()
            print(self.playtime)

    def search_for_trackable_exe(self):
        for line in self.executable_list:
            try:
                index = self.known_games[line]
                return line
            except KeyError as err:
                pass
        return None

    def store_playtime_to_file(self):
        with open('data/playtime.json', 'w') as outfile:
            json.dump(self.playtime, outfile)