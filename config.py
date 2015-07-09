__author__ = 'Administrator'
import os
def read_config():
    if not os.path.isfile("config.txt"):
        init_config()
        return 0
    else:
        with open("config.txt", "r+") as f:
            configfile = f.readlines()
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