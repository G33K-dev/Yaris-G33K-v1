
import pygame
import time
import os
import sys
import signal

print("music") 

signal.signal(signal.SIGINT, signal.SIG_IGN)

MUSIC_CREDIT = "Music by Nico B"


def get_resource(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def play_sound():
    pygame.mixer.init()

    sound = get_resource("yaris.mp3")

    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(-1)

    while True:
        time.sleep(10)


def volume_up():
    pygame.mixer.music.set_volume(1.0)


def volume_down():
    current_volume = pygame.mixer.music.get_volume()
    pygame.mixer.music.set_volume(max(0.0, current_volume - 0.1))


def set_volume(volume):
    pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))


def mute():
    pygame.mixer.music.set_volume(0.0)


def start():
    play_sound()

