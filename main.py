import pygame
from MODULES.init import CONFIG
from MODULES.RENDER.main import main_game_loop
from MODULES.START_SCREEN.start_screen import Start_Scr
from MODULES.audio import Audio_Player

size = (CONFIG["pygame"]["width"], CONFIG["pygame"]["height"])
f_size = (CONFIG["pygame"]["f_width"], CONFIG["pygame"]["f_height"])

if __name__ == "__main__":
    pygame.init()
    audio = Audio_Player()


    if CONFIG["pygame"]["fullscreen"] == "Yes":
        scr = pygame.display.set_mode((int(f_size[0]), int(f_size[1])), pygame.FULLSCREEN)
    else:
        scr = pygame.display.set_mode((int(size[0]), int(size[1])))

    size = scr.get_size()

    flag = Start_Scr(scr, size, audio)
    if flag == "main_game":
        main_game_loop(scr, size, audio)

    audio.stop_music()
    pygame.quit()
