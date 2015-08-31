__author__ = 'Administrator'
import os

zipoption = 0

def read_config():
    global zipoption
    check_if_config_valid()
    with open("config.txt", "r+") as f:
        configfile = f.read().split("\n")
        line = configfile[0].split("=")
        zipoption = int(line[1])
        return zipoption

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
    seen = set()
    history = [x for x in history if x not in seen and not seen.add(x)][-20:]
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
