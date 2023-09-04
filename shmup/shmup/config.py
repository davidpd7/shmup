import pygame    



class Config:

    __instance = None

@staticmethod
def instance():
    if Config.__instance is None:
        Config()
    return Config.__instance


def __init__(self):
    if Config.__instance is None:
        Config.__instance = self
    else:
        raise Exception ("Config only can be instanciated once") 