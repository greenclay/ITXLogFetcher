__author__ = 'Yuki Sawa, yukisawa@gmail.com'
import os

""" Manages The reading/writing of config.txt and history.txt

    config.txt - consists of one line with either zip=0 or zip=1
                 zip=1 means the app will start with "yes" for the "Archive logs into a zip file" option
                 zip=0 means it will start with "no"
    history.txt - Holds a history of the server names typed into the "Server" box
                  A servername is saved to history.txt when a user pushes "Save selected files to folder"
                  Saves the last number_of_servernames_to_save_in_history typed in server names
"""
zipoption = 0 # default zip option when intializing config.txt
number_of_servernames_to_save_in_history = 20

""" read config.txt """
def read_config():
    global zipoption
    check_if_config_valid()
    with open("config.txt", "r+") as f:
        configfile = f.read().split("\n")
        line = configfile[0].split("=")
        zipoption = int(line[1])
        return zipoption

""" Check if config.txt exists and is in the right format, which is one line that consists of either "zip=1" or "zip=0"
    If its not in the right format or does not exist then create and intialize a history.txt
"""
def check_if_config_valid():
    if not os.path.isfile("config.txt"):
        init_config()
    with open("config.txt", "r") as myfile:
        configfile = myfile.read().split("\n")
        if configfile[0] != "zip=0" and configfile[0] != "zip=1":
            init_config()

def init_config():
    with open("config.txt", "w") as configfile:
        configfile.write("zip=0")


def write_config(passed_zipoption):
    global zipoption
    with open("config.txt", "w") as configfile:
        configfile.write("zip=" + str(passed_zipoption))
        zipoption = passed_zipoption


def write_servername_history(history):
    global number_of_servernames_to_save_in_history
    seen = set()
    # get the last number_of_servernames_to_save_in_history servernames typed in and save them to history.txt
    history = [x for x in history if x not in seen and not seen.add(x)][-number_of_servernames_to_save_in_history:]
    with open("history.txt", "r+") as myfile:
        for line in history:
            myfile.write(line + "\n")


def read_servername_history():
    if not os.path.isfile("history.txt"):
        open("history.txt", "w")

    with open("history.txt", "r+") as myfile:
        history = myfile.read().split("\n")
        history = [x for x in history if x != '']
        return history
