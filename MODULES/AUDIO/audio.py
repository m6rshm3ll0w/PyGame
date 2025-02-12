import pygame
from MODULES.init import CONFIG

class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()

    def load_music(self, music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(0.3)

    def play_music(self):
        self.is_running = True
        pygame.mixer.music.play(-1)

    def pause_unpause_music(self):
        if self.is_running is False:
            pygame.mixer.music.unpause()
            self.is_running = True

        elif self.is_running is True:
            pygame.mixer.music.pause()
            self.is_running = False


    def stop_music(self):
        pygame.mixer.music.stop()

    def run(self, path=CONFIG["dirs"]["sounds"]["start_screen"]):
        self.load_music(path)
        self.play_music()
