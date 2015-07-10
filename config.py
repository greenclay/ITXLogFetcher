__author__ = 'Administrator'
import os


def read_config():
    if not os.path.isfile("config.txt"):
        init_config()
        return 0
    else:
        with open("config.txt", "r+") as f:
            configfile = f.read().split("\n")
            if len(configfile) == 0 or len(configfile) > 1:
                init_config()
                return 0
            else:
                line = configfile[0].split("=")
                zipoption = int(line[1])
                if zipoption == 0 or zipoption == 1:
                    return zipoption
                else:
                    init_config()
                    return 0


def init_config():
    with open("config.txt", "w") as configfile:
        configfile.write("zip=0")


def write_config(zipoption):
    with open("config.txt", "w") as configfile:
        configfile.write("zip=" + str(zipoption))


def write_servername_history(history):
    seen = set()
    history = [x for x in history if x not in seen and not seen.add(x)][-17:]
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
