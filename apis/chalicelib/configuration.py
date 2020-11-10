import os
from configparser import ConfigParser

configur = ConfigParser()
config_path = f"{os.path.dirname(os.path.abspath(__file__))}/config.ini"
configur.read(config_path)

def get_config(config_key):
    return configur.get(os.getenv("ENV","dev"),config_key)